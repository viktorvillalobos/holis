from django.core.files.storage import default_storage

import pytest
import uuid
from model_bakery import baker

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
        user.company_id, user.id, one_to_one_room.uuid, text
    )

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_uuid == one_to_one_room.uuid
    assert isinstance(message.uuid, uuid.UUID)


@pytest.mark.django_db(transaction=True)
def test_create_message_is_successful(one_to_one_room, user):
    text = "This is a test message"
    message = chat_services.create_message(
        user.company_id, user.id, one_to_one_room.uuid, text
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
