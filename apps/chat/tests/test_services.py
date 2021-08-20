from django.core.files.storage import default_storage

import pytest
import uuid
from model_bakery import baker
from unittest import mock

from apps.chat.lib.dataclasses import RoomData
from apps.users.tests import baker_recipes as user_recipes

from .. import services as chat_services
from ..context.providers import message as message_providers
from ..context.providers import room as room_providers
from . import baker_recipes as chat_recipes


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_message_async_is_successful(one_to_one_room, user):
    text = "This is a test message"
    message = await chat_services.create_message_async(
        user.company_id, user.id, one_to_one_room.uuid, text, app_uuid=uuid.uuid4()
    )

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_uuid == one_to_one_room.uuid
    assert isinstance(message.uuid, uuid.UUID)


@pytest.mark.django_db(transaction=True)
def test_create_message_is_successful(one_to_one_room, user):
    text = "This is a test message"
    message = chat_services.create_message(
        user.company_id, user.id, one_to_one_room.uuid, text, app_uuid=uuid.uuid4()
    )

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_uuid == one_to_one_room.uuid
    assert isinstance(message.uuid, uuid.UUID)


class TestGetRecentsRooms:
    @pytest.mark.skip("TODO: this not use a room to serialize")
    def test_get_recents_rooms(self, mocker):
        mocked_get_recents_messages_values_by_user_id = mocker.patch(
            f"{message_providers.__name__}.get_recents_messages_values_by_user_id"
        )

        mocked_get_recents_messages_values_by_user_id.return_value = [
            {"room_uuid": uuid.uuid4(), "text": "this is a text"}
        ]

        mocked_get_rooms_by_uuids_in_bulk = mocker.patch(
            f"{room_providers.__name__}.get_rooms_by_uuids_in_bulk"
        )

        expected_kwargs = dict(
            company_id=1, user_id=1, is_one_to_one=True, limit=5, search=None
        )

        results = chat_services.get_recents_rooms_by_user_id(**expected_kwargs)

        mocked_get_recents_messages_values_by_user_id.assert_called_once_with(
            **expected_kwargs
        )

        mocked_get_rooms_by_uuids_in_bulk.assert_called_once()

        assert isinstance(results, list)


@mock.patch("apps.chat.services.room_providers.get_room_with_members_by_uuid")
def test_get_room_with_members_by_uuid(mocked_provider):
    mocked_provider.return_value = mock.MagicMock()

    kwargs = dict(company_id=mock.Mock(), room_uuid=mock.Mock())

    result = chat_services.get_room_with_members_by_uuid(**kwargs)

    mocked_provider.assert_called_once_with(**kwargs)
    assert isinstance(result, RoomData)


@mock.patch("apps.chat.services.room_providers.update_room_image_by_uuid")
def test_update_room_image_by_uuid(mocked_provider):
    mocked_provider.return_value = mock.MagicMock()

    kwargs = dict(company_id=mock.Mock(), room_uuid=mock.Mock(), image=mock.Mock())

    result = chat_services.update_room_image_by_uuid(**kwargs)

    assert isinstance(result, RoomData)
    mocked_provider.assert_called_once_with(**kwargs)


@mock.patch("apps.chat.services.room_providers.remove_user_from_room_by_uuid")
def test_remove_user_from_room_by_uuid(mocked_provider):
    mocked_provider.return_value = None
    kwargs = dict(company_id=mock.Mock(), user_id=mock.Mock(), room_uuid=mock.Mock())

    result = chat_services.remove_user_from_room_by_uuid(**kwargs)

    assert result is None
    mocked_provider.assert_called_once_with(**kwargs)


@mock.patch("apps.chat.services.user_services.get_users_by_ids_in_bulk")
@mock.patch(
    "apps.chat.services.room_providers.get_or_create_one_to_one_conversation_room_by_members_ids"
)
def test_get_or_create_one_to_one_conversation_room_by_members_ids(
    mocked_provider, mocked_user_service
):
    mocked_to_user_id = mock.Mock()
    mocked_from_user_id = mock.Mock()
    mocked_company_id = mock.Mock()

    mocked_user_service.return_value = {
        mocked_to_user_id: mocked_to_user_id,
        mocked_from_user_id: mocked_from_user_id,
    }

    kwargs = dict(
        company_id=mocked_company_id,
        to_user_id=mocked_to_user_id,
        from_user_id=mocked_from_user_id,
    )

    result = chat_services.get_or_create_one_to_one_conversation_room_by_members_ids(
        **kwargs
    )

    mocked_provider.assert_called_once_with(**kwargs)

    mocked_user_service.assert_called_once_with(
        company_id=mocked_company_id, users_ids={mocked_to_user_id, mocked_from_user_id}
    )

    assert isinstance(result, RoomData)


@mock.patch("apps.chat.services.user_services.get_users_by_ids_in_bulk")
@mock.patch(
    "apps.chat.services.room_providers.get_or_create_many_to_many_conversation_room_by_members_ids"
)
def test_get_or_create_many_to_many_conversation_room_by_members_ids(
    mocked_provider, mocked_user_service
):
    mocked_user1 = mock.Mock()
    mocked_user2 = mock.Mock()
    mocked_user3 = mock.Mock()
    mocked_company_id = mock.Mock()

    mocked_user_service_return = {
        mocked_user1: mocked_user1,
        mocked_user2: mocked_user2,
        mocked_user3: mocked_user3,
    }

    members_ids = list(mocked_user_service_return.values())

    mocked_user_service.return_value = mocked_user_service_return

    kwargs = dict(company_id=mocked_company_id, members_ids=members_ids)

    result = chat_services.get_or_create_many_to_many_conversation_room_by_members_ids(
        **kwargs
    )

    mocked_provider.assert_called_once_with(**kwargs)

    mocked_user_service.assert_called_once_with(
        company_id=mocked_company_id, users_ids=members_ids
    )

    assert isinstance(result, RoomData)
