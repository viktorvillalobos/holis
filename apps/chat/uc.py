import uuid

from apps.chat import models as chat_models
from apps.users import models as users_models
from apps.utils import openfire
from django.db import DatabaseError, models, transaction


class ChannelCreationXMPPError(Exception):
    pass


class ChannelCreationDBError(Exception):
    pass


class NonExistentMemberException(Exception):
    pass


class ChannelUCBase:
    def execute(self):
        sid = transaction.savepoint()

        try:
            channel = self._create_django_channel()
        except DatabaseError as ex:
            raise ChannelCreationDBError(str(ex))

        try:
            self._create_xmpp_channel(channel)
            transaction.savepoint_commit(sid)
            self.channel = channel
            return self
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            raise ChannelCreationXMPPError(str(ex))

    def get_channel(self):
        return self.channel


class CreateOneToOneChannelUC(ChannelUCBase):
    def __init__(self, company, members) -> None:
        self.company = company
        self.members = self.get_members(members)
        self.name = str(uuid.uuid4())

    def get_members(self, members):
        result = []
        for x in members:
            try:
                x = users_models.User.objects.get(id=x)
                result.append(x)
            except users_models.User.DoesNotExist:
                raise NonExistentMemberException('User does not exist')

        return result

    def _create_django_channel(self):
        existent = self.get_existent_channel()
        if existent:
            return existent

        data = {
            "company": self.company,
            "is_one_to_one": True,
            "name": self.name,
            "any_can_invite": False,
            "members_only": True,
            "max_users": 2,
        }
        channel = chat_models.Channel.objects.create(**data)

        for x in self.members:
            channel.members.add(x)
        channel.save()

        return channel

    def _create_xmpp_channel(self, channel):
        muc = openfire.Muc()
        muc.add_room(
            str(channel.id),
            name=str(channel.id),
            description="one to one channel",
            maxusers=channel.max_users,
            members=[str(x.jid) for x in self.members],
        )

    def get_existent_channel(self):
        try:
            return (
                chat_models.Channel.objects.filter(
                    members__in=self.members, is_one_to_one=True
                )
                .annotate(num_members=models.Count('members'))
                .filter(num_members=2)
                .first()
            )
        except chat_models.Channel.DoesNotExist:
            pass
