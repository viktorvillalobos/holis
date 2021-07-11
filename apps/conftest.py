from django.conf import settings

import pytest
from model_bakery import baker

from apps.users.context.models import User

baker.generators.add(
    "apps.utils.fields.LowerCharField", "model_bakery.random_gen.gen_string"
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return baker.make(settings.AUTH_USER_MODEL)
