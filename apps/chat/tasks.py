from typing import Any, Union

from celery import shared_task

import logging
from asgiref.sync import sync_to_async
from uuid import UUID

from . import services as chat_services

logger = logging.getLogger(__name__)


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
    logger.info("set_room_user_read_task")
    chat_services.set_room_user_read(
        company_id=company_id, user_id=user_id, room_uuid=room_uuid
    )


@shared_task
def send_message_to_devices_by_user_ids_task(
    company_id: int, room_uuid: Union[UUID, str], serialized_message: dict[str, Any]
):
    logger.info("send_message_to_devices_by_user_ids_task")
    chat_services.send_message_to_devices_by_user_ids(
        company_id=company_id,
        room_uuid=room_uuid,
        serialized_message=serialized_message,
    )


send_message_to_devices_by_user_ids_task_async = sync_to_async(
    send_message_to_devices_by_user_ids_task.delay
)
