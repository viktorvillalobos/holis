import datetime as dt
import uuid

from apps.users.models import User, Status
from apps.utils import openfire
from django.db import DatabaseError, transaction


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
            user = self.create_django_user()
        except DatabaseError as ex:
            raise UserCreationDBError(str(ex))

        try:
            self._create_xmpp_user()
            self._add_user_to_group()
            self._create_base_statuses(user)
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

    def _create_base_statuses(self, user):
        base = [
            {
                "company": self.company,
                "user": user,
                "icon": "💻",
                "text": "Available",
                "is_active": True,
            },
            {
                "company": self.company,
                "user": user,
                "icon": "🤝",
                "text": "Metting",
                "is_active": False,
            },
            {
                "company": self.company,
                "user": user,
                "icon": "😋",
                "text": "Having launch",
                "is_active": False,
            },
            {
                "company": self.company,
                "user": user,
                "icon": "👻",
                "text": "Absent",
                "is_active": False,
            },
        ]

        objects = [Status(**x) for x in base]

        Status.objects.bulk_create(objects)
