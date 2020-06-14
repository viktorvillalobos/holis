import datetime as dt
from apps.users.models import User
from apps.utils import openfire


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
        self.birthday = birthday or dt.datetime.now().date()

    def execute(self):
        self.user = self.create_django_user()
        self.create_xmpp_account()

    def create_django_user(self):
        return User.objects.create_user(
            company=self.company, email=self.email, username=self.email
        )

    def create_xmpp_account(self):
        client = openfire.users.Users()
        client.add_user(self.username, self.password, email=self.email)
