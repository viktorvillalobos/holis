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


@pytest.mark.django_db
def test_get_unavailable_users_by_company_id():
    ten_minutes_ago_date = datetime.now() - timedelta(minutes=10)

    inactive_user = user_recipes.user_viktor.make(last_seen=ten_minutes_ago_date)
    active_user = user_recipes.user_julls.make(last_seen=datetime.now())
    inactive_user_outside_area = baker.make(
        "users.User",
        company=inactive_user.company,
        current_area=None,
        last_seen=ten_minutes_ago_date,
    )

    expected_result = [inactive_user_outside_area, inactive_user]

    result = user_services.get_unavailable_users_by_company_id(
        company_id=active_user.company_id
    )

    assert expected_result == result
