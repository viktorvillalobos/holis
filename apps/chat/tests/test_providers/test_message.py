import pytest
from model_bakery import baker

from apps.chat.providers import message as message_providers

from .. import baker_recipes as chat_recipes


@pytest.mark.skip("TODO: this not use a room to serialize")
@pytest.mark.django_db
def test_get_recents_messages_values_by_user_id():
    message = chat_recipes.adslab_message_one_to_one.make()
    room_1 = message.room
    room_2 = baker.make(
        "chat.Room",
        is_one_to_one=True,
        members=message.room.members.all(),
        company_id=message.company_id,
    )

    baker.make("chat.message", room=room_1, company_id=message.company_id, _quantity=2)

    room_1_last_message = baker.make(
        "chat.message", room=room_1, company_id=message.company_id
    )

    baker.make("chat.message", room=room_2, company_id=message.company_id, _quantity=2)

    room_2_last_message = baker.make(
        "chat.message", room=room_2, company_id=message.company_id
    )

    result = message_providers.get_recents_messages_values_by_user_id(
        company_id=message.company_id,
        user_id=message.user_id,
        is_one_to_one=True,
        page_size=2,
    )

    expected_result = {room_2_last_message.created, room_1_last_message.created}

    assert {message["created"] for message in result} == expected_result
