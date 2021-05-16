from django.conf import settings

import pytest
from datetime import datetime, timedelta
from model_bakery import baker

from apps.core.tests import baker_recipes as core_recipes

from .. import services as user_services
from . import baker_recipes as user_recipes


@pytest.mark.django_db
def test_service_serialize_user(active_user: settings.AUTH_USER_MODEL) -> None:
    serialized_user = user_services.serialize_user(active_user)

    assert isinstance(serialized_user, dict)
