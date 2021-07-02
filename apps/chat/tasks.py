from typing import Union

from celery import shared_task

from uuid import UUID

from . import services as chat_services


@shared_task
def set_messages_readed_by_room_and_user_task(
    *, company_id: int, room_uuid: Union[str, UUID], user_id: int
) -> int:
    """
    Allow to mark unreaded messages readed by user in room
    Returns the total updated chat messages
    """
    return chat_services.set_messages_readed_by_room_and_user(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id
    )


@shared_task
def set_room_user_read_task(
    *, company_id: int, user_id: int, room_uuid: Union[str, UUID]
) -> None:
    chat_services.set_room_user_read(
        company_id=company_id, user_id=user_id, room_uuid=room_uuid
    )
