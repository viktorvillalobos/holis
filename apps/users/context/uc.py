from django.db import DatabaseError, transaction

import datetime as dt

from .models import Status, User


class UserCreationXMPPError(Exception):
    pass


class UserCreationDBError(Exception):
    pass


class UserUCBase:
    pass


class CreateUser(UserUCBase):
    def __init__(
        self, company: str, email: str, password: str, birthday=None, **fields
    ) -> "CreateUser":
        """
        :param company: company
        :param email: email of the user
        :param password: hashed password
        :param fields: aditional fields
        """
        self.company = company
        self.email = email
        self.password = password
        self.username = email
        self.birthday = birthday or dt.datetime.now().date()
        self.fields = fields

    def execute(self) -> User:

        sid = transaction.savepoint()

        try:
            user = self.create_django_user()
            self._create_base_statuses(user)
        except DatabaseError as ex:
            raise UserCreationDBError(str(ex))

        transaction.savepoint_rollback(sid)

        return user

    def create_django_user(self):
        user = User.objects.create_user(
            company=self.company,
            email=self.email,
            username=self.email,
            birthday=self.birthday,
            **self.fields,
        )

        user.password = self.password
        user.save()

        return user

    def _create_base_statuses(self, user) -> None:
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
