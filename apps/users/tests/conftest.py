from django.conf import settings

import pytest
from model_bakery import baker


@pytest.fixture
def active_user():
    return baker.make(settings.AUTH_USER_MODEL)
