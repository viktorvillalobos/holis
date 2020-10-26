import datetime as dt
from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, SubFactory, fuzzy, post_generation


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    birthday = fuzzy.FuzzyDate(
        start_date=dt.date(1970, 1, 1),
        end_date=dt.date.today() - dt.timedelta(days=20 * 365),
    )

    company = SubFactory("apps.core.tests.factories.CompanyFactory")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
