from typing import Optional

from django.db import DatabaseError, models

import uuid

from apps.chat import models as chat_models
from apps.users import models as users_models


class RoomCreationXMPPError(Exception):
    pass


class RoomCreationDBError(Exception):
    pass


class NonExistentMemberException(Exception):
    pass


class RoomUCBase:
    def execute(self):
        try:
            self.room = self.get_or_create_room()
        except DatabaseError as ex:
            raise RoomCreationDBError(str(ex))
        return self

    def get_room(self):
        return self.room


class RoomCreate(RoomUCBase):
    def __init__(self, company, members_ids) -> None:
        self.company = company
        self.members_ids = members_ids
        self.members = self.get_members()
        self.name = str(uuid.uuid4())

    def get_members(self):
        results = users_models.User.objects.filter(
            id__in=self.members_ids, company=self.company
        )

        if results.count() != len(self.members_ids):
            raise NonExistentMemberException("User does not exist")

        return results

    def get_or_create_room(self):
        instance = self.get_room()
        if instance:
            return instance

        data = {
            "company": self.company,
            "is_one_to_one": True,
            "name": self.name,
            "any_can_invite": False,
            "members_only": True,
            "max_users": 2,
        }
        channel = chat_models.Room.objects.create(**data)

        for x in self.members:
            channel.members.add(x)
        channel.save()

        return channel

    def get_room(self) -> Optional[chat_models.Room]:
        return (
            chat_models.Room.objects.filter(
                members__in=self.members, is_one_to_one=True
            )
            .annotate(num_members=models.Count("members"))
            .filter(num_members=2)
            .first()
        )
