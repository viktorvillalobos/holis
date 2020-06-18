from django.db import DatabaseError, transaction


class ChannelCreationXMPPError(Exception):
    pass


class ChannelCreationDBError(Exception):
    pass


class ChannelUCBase:
    pass


class CreateChatUC:
    def execute(self):
        sid = transaction.savepoint()

        try:
            self._create_django_user = self.create_django_user()
        except DatabaseError as ex:
            raise ChannelCreationDBError(str(ex))

        try:
            self._create_xmpp_user()
            self._add_user_to_group()
            transaction.savepoint_commit(sid)
        except Exception:
            transaction.savepoint_rollback(sid)
            raise ChannelCreationXMPPError(
                "Error creating user in XMPP server"
            )

    def create_django_channel(self):
        pass

    def create_xmpp_channel(self):
        pass
