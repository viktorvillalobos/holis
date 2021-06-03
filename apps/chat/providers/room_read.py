from typing import Union

from django.utils import timezone

from uuid import UUID

from apps.chat.models import RoomRead


def get_room_read_by_user_and_room_uuid(
    *, company_id: int, room_uuid: Union[UUID, str], user_id: int
) -> RoomRead:
    """ Return the room read for an user in a group """
    return RoomRead.objects.get(
        company_id=company_id, user_id=user_id, room_uuid=room_uuid
    )


def update_or_create_room_read_by_user_and_room_uuid(
    *, company_id: int, room_uuid: Union[UUID, str], user_id: int
) -> tuple[RoomRead, bool]:
    """ Update or create the room read for a specific room and user """
    room_read, created = RoomRead.objects.update_or_create(
        company_id=company_id,
        user_id=user_id,
        room_uuid=room_uuid,
        defaults={"timestamp": timezone.now()},
    )

    return room_read, created
