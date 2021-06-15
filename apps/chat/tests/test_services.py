from django.core.files.storage import default_storage

import pytest
import uuid
from model_bakery import baker

from apps.users.tests import baker_recipes as user_recipes

from .. import services as chat_services
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


@pytest.mark.skip("Flaky")
@pytest.mark.django_db()
class TestGetRecentsRooms:
    def setup_method(self):
        self.user_viktor = user_recipes.user_viktor.make()
        self.user_julls = user_recipes.user_julls.make()
        self.user_tundi = user_recipes.user_tundi.make()

        self.room_viktor_julls = chat_recipes.adslab_room_one_to_one.make(
            members=[self.user_viktor, self.user_julls]
        )

        self.room_viktor_tundi = chat_recipes.adslab_room_one_to_one.make(
            name="room-viktor-tundi", members=[self.user_viktor, self.user_tundi]
        )

        self.room_viktor_julls_message = chat_recipes.adslab_message_one_to_one.make()
        self.room_viktor_tundi_message = chat_recipes.adslab_message_one_to_one.make(
            room=self.room_viktor_tundi
        )

    def test_get_recents_rooms(self):

        expected_result = [
            {
                "room": self.room_viktor_tundi.uuid,
                "avatar_thumb": self.user_tundi.avatar_thumb,
                "id": self.user_tundi.id,
                "name": self.user_tundi.name,
                "message": self.room_viktor_tundi_message.text,
                "created": self.room_viktor_tundi_message.created,
            },
            {
                "room": self.room_viktor_julls.uuid,
                "avatar_thumb": self.user_julls.avatar_thumb,
                "id": self.user_julls.id,
                "name": self.user_julls.name,
                "message": self.room_viktor_julls_message.text,
                "created": self.room_viktor_julls_message.created,
            },
        ]
        results = chat_services.get_recents_rooms_by_user_id(
            user_id=self.user_viktor.id
        )

        assert results == expected_result

    def test_get_recents_rooms_with_limit(self):

        expected_result = [
            {
                "room": self.room_viktor_tundi.uuid,
                "avatar_thumb": self.user_tundi.avatar_thumb,
                "id": self.user_tundi.id,
                "name": self.user_tundi.name,
                "message": self.room_viktor_tundi_message.text,
                "created": self.room_viktor_tundi_message.created,
            }
        ]

        results = chat_services.get_recents_rooms_by_user_id(
            user_id=self.user_viktor.id, limit=1
        )

        assert results == expected_result
