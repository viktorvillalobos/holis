import pytest
import uuid
from unittest import mock

from apps.chat.context.models import Room
from apps.users.tests import baker_recipes as users_recipes

from ...context.providers import room as room_providers
from .. import baker_recipes as chat_recipes


@pytest.mark.django_db
class TestGetOrCreateOneToOneConversationRoom:
    def setup_method(self):
        self.existent_room = chat_recipes.adslab_room_one_to_one.make()
        self.users = list(
            self.existent_room.members.values_list("id", flat=True).order_by("id")
        )

    def test_get_or_create_one_to_one_conversation_room_by_members_ids_returns_existent_room(
        self, django_assert_num_queries
    ):
        with django_assert_num_queries(num=1):
            room = room_providers.get_or_create_one_to_one_conversation_room_by_members_ids(
                company_id=self.existent_room.company_id,
                to_user_id=self.users[0],
                from_user_id=self.users[1],
            )

        assert room == self.existent_room
        assert Room.objects.count() == 1

    def test_get_or_create_one_to_one_conversation_room_by_members_ids_create_a_new_instance(
        self, django_assert_num_queries
    ):
        to_user_id = self.users[0]
        other_user = users_recipes.user_tundi.make()

        expected_room_name = f"Tundi, Víktor"

        with django_assert_num_queries(num=3):
            new_room = room_providers.get_or_create_one_to_one_conversation_room_by_members_ids(
                company_id=self.existent_room.company_id,
                to_user_id=to_user_id,
                from_user_id=other_user.id,
            )

        assert new_room is not self.existent_room

        expected_one_to_one_conversation_fields = {
            "name": expected_room_name,
            "is_one_to_one": True,
            "is_conversation": True,
            "any_can_invite": False,
            "members_only": True,
            "max_users": 2,
        }

        for field, value in expected_one_to_one_conversation_fields.items():
            assert getattr(new_room, field) == value


@pytest.mark.django_db
class TestGetOrCreateManyToManyConversationRoom:
    def test_get_or_create_many_to_many_conversation_room_returns_existent_room(
        self, django_assert_num_queries
    ):
        existent_room = chat_recipes.adslab_conversation_room_many_to_many.make()
        users = list(existent_room.members.values_list("id", flat=True).order_by("id"))

        with django_assert_num_queries(num=1):
            room = room_providers.get_or_create_many_to_many_conversation_room_by_members_ids(
                company_id=existent_room.company_id, members_ids=set(users)
            )

        assert room == existent_room

    def test_get_or_create_many_to_many_conversation_room_create_a_new_room(
        self, django_assert_num_queries
    ):

        # Create users
        user1 = users_recipes.user_julls.make()
        user2 = users_recipes.user_tundi.make()
        user3 = users_recipes.user_viktor.make()
        members_ids = {user1.id, user2.id, user3.id}

        expected_room_name = f"Julls, Tundi, Víktor"

        with django_assert_num_queries(num=3):
            new_room = room_providers.get_or_create_many_to_many_conversation_room_by_members_ids(
                company_id=user1.company_id, members_ids=members_ids
            )

        expected_one_to_one_conversation_fields = {
            "name": expected_room_name,
            "is_one_to_one": False,
            "is_conversation": True,
            "any_can_invite": False,
            "members_only": True,
            "max_users": 3,
        }

        for field, value in expected_one_to_one_conversation_fields.items():
            assert getattr(new_room, field) == value


@pytest.mark.django_db
def test_remove_user_from_room_by_uuid(django_assert_num_queries):
    room = chat_recipes.adslab_room_one_to_one.make()
    room_users = list(room.members.all())

    assert len(room_users) == 2

    user_to_remove = room_users[0]
    expected_result = [room_users[1]]

    with django_assert_num_queries(num=3):
        room_providers.remove_user_from_room_by_uuid(
            company_id=room.company_id, user_id=user_to_remove.id, room_uuid=room.uuid
        )

    assert list(room.members.all()) == expected_result
