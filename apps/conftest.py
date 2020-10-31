import pytest
from django.conf import settings
from model_bakery import baker

from apps.users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return baker.make(settings.AUTH_USER_MODEL)
