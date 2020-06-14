import datetime as dt
import uuid
from django.db import DatabaseError, transaction

from apps.users.models import User
from apps.utils import openfire


class UserCreationXMPPError(Exception):
    pass


class UserCreationDBError(Exception):
    pass


class UserUCBase:
    pass


class UserCreateUC(UserUCBase):
    def __init__(self, company, email, password, birthday=None, **args):
        """
        :param company: company
        :param email: email of the user
        :param password: password
        :param args: Aditional data
        """
        self.company = company
        self.email = email
        self.password = password
        self.username = email
        self.jid = str(uuid.uuid4())
        self.birthday = birthday or dt.datetime.now().date()

    def execute(self):

        sid = transaction.savepoint()

        try:
            self._create_django_user = self.create_django_user()
        except DatabaseError as ex:
            raise UserCreationDBError(str(ex))

        try:
            self._create_xmpp_user()
            self._add_user_to_group()
            transaction.savepoint_commit(sid)
        except Exception:
            transaction.savepoint_rollback(sid)
            raise UserCreationXMPPError("Error creating user in XMPP server")

    def create_django_user(self):
        return User.objects.create_user(
            company=self.company,
            email=self.email,
            username=self.email,
            birthday=self.birthday,
            jid=self.jid,
        )

    def _create_xmpp_user(self):
        client = openfire.Users()
        client.add_user(self.jid, self.password, email=self.email)

    def _add_user_to_group(self):
        client = openfire.Users()
        client.add_user_groups(self.jid, [self.company.code])
