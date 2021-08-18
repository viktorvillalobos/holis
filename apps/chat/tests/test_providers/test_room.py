import pytest

from ...context.providers import room as room_providers
from .. import baker_recipes as chat_recipes


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
