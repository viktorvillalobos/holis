import pytest
import uuid

from ..services import create_message


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_message_is_successful(room, user):
    text = "This is a test message"
    message = await create_message(user.company_id, user.id, room.id, text)

    assert message.text == text
    assert message.company_id == user.company_id
    assert message.room_id == room.id
    assert isinstance(message.id, uuid.UUID)
