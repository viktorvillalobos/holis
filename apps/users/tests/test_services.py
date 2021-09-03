from django.conf import settings
from django.utils import timezone

import pytest
from datetime import date, datetime, timedelta
from model_bakery import baker
from unittest import mock

from apps.core.tests import baker_recipes as core_recipes
from apps.users.context.providers.status import (
    inactivate_all_user_status_by_user_id,
    set_active_status_by_user_and_status_id,
)
from apps.users.lib.constants import USER_NOTIFICATION_CHANNEL_KEY

from .. import services as user_services
from . import baker_recipes as user_recipes

USER_SERVICES_PATH = "apps.users.services"


@pytest.mark.django_db
def test_service_serialize_user() -> None:
    user = user_recipes.user_viktor.make()
    serialized_user = user_services.serialize_user(user)

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


def test_update_user_profile(mocker):
    mocked_provider = mocker.patch(
        f"{USER_SERVICES_PATH}.user_providers.update_user_profile"
    )

    expected_kwargs = dict(
        id=-999,
        company_id=-999,
        birthday=date(1991, 2, 15),
        email="other@email.com",
        name="Linus Torvalds",
        position="Linux Creator",
    )

    user_services.update_user_profile(**expected_kwargs)

    mocked_provider.assert_called_once_with(**expected_kwargs)


@mock.patch("apps.users.services.build_dataclass_from_model_instance")
@mock.patch("apps.users.services.user_providers.get_users_by_ids")
def test_get_users_by_ids_in_bulk(
    mocked_provider, mocked_build_dataclass_from_model_instance
):

    mocked_provider.return_value = [mock.MagicMock(), mock.MagicMock()]

    mocked_users_ids = [mock.Mock(), mock.Mock()]
    kwargs = dict(company_id=mock.Mock(), users_ids=mocked_users_ids)

    result = user_services.get_users_by_ids_in_bulk(**kwargs)

    mocked_provider.assert_called_once_with(**kwargs)

    assert mocked_build_dataclass_from_model_instance.call_count == 2
    assert isinstance(result, dict)


@mock.patch("apps.users.services.user_invitation_providers.create_users_invitations")
def test_create_users_invitations(mocked_provider):

    kwargs = dict(company_id=mock.Mock(), user_id=mock.Mock(), emails=[mock.Mock()])

    result = user_services.create_users_invitations(**kwargs)

    assert isinstance(result, list)

    mocked_provider.assert_called_once_with(**kwargs)
