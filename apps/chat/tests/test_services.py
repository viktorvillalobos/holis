import pytest
import uuid
from model_bakery import baker

from ..services import create_message, create_message_async, get_recents_rooms


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_message_async_is_successful(one_to_one_room, user):
    text = "This is a test message"
    message = await create_message_async(
        user.company_id, user.id, one_to_one_room.uuid, text
    )

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_uuid == one_to_one_room.uuid
    assert isinstance(message.id, uuid.UUID)


@pytest.mark.django_db(transaction=True)
async def test_create_message_is_successful(one_to_one_room, user):
    text = "This is a test message"
    message = create_message(user.company_id, user.id, one_to_one_room.uuid, text)

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_uuid == one_to_one_room.uuid
    assert isinstance(message.id, uuid.UUID)


@pytest.mark.django_db
def test_get_recents_rooms(one_to_one_room, user, user2):
    expected_result = [
        {
            "room": one_to_one_room.uuid,
            "avatar_thumb": user2.avatar_thumb,
            "id": user2.id,
            "name": user.name,
        }
    ]
    baker.make("chat.Message", user=user, room=one_to_one_room)
    results = get_recents_rooms(user.pk)

    assert results == expected_result
