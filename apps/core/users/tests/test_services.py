from django.conf import settings
from django.utils import timezone

import pytest
from datetime import datetime, timedelta
from model_bakery import baker

from apps.core.tests import baker_recipes as core_recipes
from apps.users.lib.constants import USER_NOTIFICATION_CHANNEL_KEY
from apps.users.providers.status import (
    inactivate_all_user_status_by_user_id,
    set_active_status_by_user_and_status_id,
)

from .. import services as user_services
from . import baker_recipes as user_recipes

USER_SERVICES_PATH = "apps.users.services"


@pytest.mark.django_db
def test_service_serialize_user(active_user: settings.AUTH_USER_MODEL) -> None:
    serialized_user = user_services.serialize_user(active_user)

    assert isinstance(serialized_user, dict)


def test_get_user_avatar_thumb():
    user = baker.prepare("users.User")
    avatar_image_name = "custom-avatar.png"
    user.avatar = avatar_image_name
    result = user_services.get_user_avatar_thumb(user=user)

    expected_result = f"{settings.MEDIA_URL}{avatar_image_name}"
    assert result == expected_result


def test_get_user_notification_channel_by_user_id():
    user_id = 999
    company_id = 111

    result = user_services.get_user_notification_channel_by_user_id(
        company_id=company_id, user_id=user_id
    )

    expected_result = USER_NOTIFICATION_CHANNEL_KEY.format(company_id, user_id)

    assert result == expected_result


def test_touch_user_by_user_and_area_id(mocker):
    mocked_provider = mocker.patch(
        f"{USER_SERVICES_PATH}.user_providers.touch_user_by_user_and_area_id"
    )
    expected_kwargs = dict(user_id=1, area_id=2, ts=timezone.now())

    user_services.touch_user_by_user_and_area_id(**expected_kwargs)

    mocked_provider.assert_called_once_with(**expected_kwargs)


def test_disconnect_user_by_id(mocker):
    mocked_provider = mocker.patch(
        f"{USER_SERVICES_PATH}.user_providers.disconnect_user_by_id"
    )
    expected_kwargs = dict(user_id=1)

    user_services.disconnect_user_by_id(**expected_kwargs)

    mocked_provider.assert_called_once_with(**expected_kwargs)


def test_set_user_status_by_user_and_status_id(mocker):
    mocked_inactive_all_user_status_by_user_id = mocker.patch(
        f"{USER_SERVICES_PATH}.status_providers.inactivate_all_user_status_by_user_id"
    )
    mocked_set_active_status_by_user_and_status_id = mocker.patch(
        f"{USER_SERVICES_PATH}.status_providers.set_active_status_by_user_and_status_id"
    )
    mocked_transaction_atomic = mocker.patch(f"{USER_SERVICES_PATH}.transaction.atomic")
    expected_kwargs_for_provider_1 = dict(company_id=1, user_id=1)
    expected_kwargs_for_provider_2 = dict(company_id=1, user_id=1, status_id=1)

    user_services.set_user_status_by_user_and_status_id(
        **expected_kwargs_for_provider_2
    )

    mocked_transaction_atomic.assert_called_once()
    mocked_inactive_all_user_status_by_user_id.assert_called_once_with(
        **expected_kwargs_for_provider_1
    )
    mocked_set_active_status_by_user_and_status_id.assert_called_once_with(
        **expected_kwargs_for_provider_2
    )


def test_get_user_active_status_from_cache_by_user_id(mocker):
    mocked_provider = mocker.patch(
        f"{USER_SERVICES_PATH}.status_providers.get_user_active_status_from_cache_by_user_id"
    )

    expected_kwargs = dict(company_id=111, user_id=999)

    user_services.get_user_active_status_from_cache_by_user_id(**expected_kwargs)

    mocked_provider.assert_called_once_with(**expected_kwargs)


def test_get_user_active_status_from_db_by_user_id(mocker):
    mocked_provider = mocker.patch(
        f"{USER_SERVICES_PATH}.status_providers.get_user_active_status_from_db_by_user_id"
    )

    expected_kwargs = dict(company_id=111, user_id=999)

    user_services.get_user_active_status_from_db_by_user_id(**expected_kwargs)

    mocked_provider.assert_called_once_with(**expected_kwargs)
