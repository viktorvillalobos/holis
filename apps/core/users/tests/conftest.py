from django.conf import settings

import pytest
from model_bakery import baker


@pytest.fixture
def active_user():
    return baker.make(settings.AUTH_USER_MODEL)


@pytest.fixture
def expected_users_fields():
    return {
        "id",
        "birthday",
        "name",
        "position",
        "statuses",
        "username",
        "avatar_thumb",
        "is_staff",
    }
