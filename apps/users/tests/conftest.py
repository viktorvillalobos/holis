from django.conf import settings

import pytest


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
