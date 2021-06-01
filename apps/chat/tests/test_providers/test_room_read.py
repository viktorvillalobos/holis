from django.utils import timezone

import pytest
from freezegun import freeze_time

from apps.chat.models import RoomRead

from ...providers import room_read as room_read_providers
from .. import baker_recipes as chat_recipes


@pytest.mark.django_db
def test_get_room_read_by_user_and_room_uuid():
    room_read = chat_recipes.adslab_room_one_to_one_room_read.make()

    result = room_read_providers.get_room_read_by_user_and_room_uuid(
        company_id=room_read.company_id,
        room_uuid=room_read.room_uuid,
        user_id=room_read.user.id,
    )

    assert result == room_read
    assert isinstance(result, RoomRead)


@freeze_time("2016-03-28 14:32:00", tz_offset=-4)
@pytest.mark.django_db
class TestUpdateOrCreateRoomRead:
    def test_update_or_create_room_read_by_user_and_room_uuid_update_only(self):
        room_read = chat_recipes.adslab_room_one_to_one_room_read.make()

        (
            result,
            created,
        ) = room_read_providers.update_or_create_room_read_by_user_and_room_uuid(
            company_id=room_read.company_id,
            room_uuid=room_read.room_uuid,
            user_id=room_read.user.id,
        )

        assert isinstance(result, RoomRead)
        assert not created

        assert RoomRead.objects.count() == 1
        assert result.timestamp == timezone.now()

    def test_update_or_create_room_read_by_user_and_room_uuid_create_only(self):
        room = chat_recipes.adslab_room_one_to_one.make()
        user = room.members.all().first()

        (
            result,
            created,
        ) = room_read_providers.update_or_create_room_read_by_user_and_room_uuid(
            company_id=room.company_id, room_uuid=room.uuid, user_id=user.id
        )

        assert isinstance(result, RoomRead)
        assert created

        assert RoomRead.objects.count() == 1
        assert result.timestamp == timezone.now()
