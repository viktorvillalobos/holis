from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.utils import timezone

import uuid
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from datetime import datetime
from twilio.rest import Client
from uuid import UUID

from apps.chat.lib.constants import ROOM_GROUP_NAME
from apps.chat.lib.dataclasses import RecentChatInfo
from apps.chat.lib.exceptions import NonExistentMemberException
from apps.users import models as users_models
from apps.users import services as user_services
from apps.utils.cache import cache

from ..chat.api import serializers
from ..chat.models import Message, Room, RoomUserRead
from .providers import devices as devices_providers
from .providers import message as message_providers
from .providers import room as room_providers


@database_sync_to_async
def create_message_async(
    company_id: int, user_id: int, room_uuid: Union[UUID, str], text: str
) -> Message:
    return message_providers.create_message(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id, text=text
    )


def create_message(company_id: int, user_id: int, room_uuid: int, text: str) -> Message:
    return message_providers.create_message(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id, text=text
    )


def _serialize_message(message):
    data = serializers.MessageWithAttachmentsSerializer(message).data

    return {
        **data,
        **{"id": str(data["id"]), "room": str(data["room"]), "type": "chat.message"},
    }


@database_sync_to_async
def serialize_message(message: Message) -> Dict[str, Any]:

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    return _serialize_message(message=message)


def get_cursored_recents_rooms_by_user_id(
    *,
    company_id: int,
    user_id: int,
    is_one_to_one: bool = True,
    search: Optional[str] = None,
    cursor: Optional[dict[str, str]] = None,
    page_size: Optional[int] = 100,
    reverse: Optional[bool] = True,
) -> tuple[List[RecentChatInfo], Optional[Dict[str, str]], Optional[Dict[str, str]]]:

    (
        recents_rooms,
        next_page_cursor,
        previous_page_cursor,
    ) = room_providers.get_recents_rooms_by_user_id(
        company_id=company_id,
        user_id=user_id,
        is_one_to_one=is_one_to_one,
        page_size=page_size,
        cursor=cursor,
        reverse=reverse,
        search=search,
    )

    recents_data = []
    for room in recents_rooms:

        members_by_id = {member.id: member for member in room.members.all()}

        last_message_user = members_by_id.pop(room.last_message_user_id)

        if is_one_to_one:
            another_user_id = list(members_by_id.keys())[0]
            chat_image_url = members_by_id[another_user_id].avatar_thumb
            chat_name = members_by_id[another_user_id].name
        else:
            raise NotImplementedError("We must implement grupal recents rooms")

        recents_data.append(
            RecentChatInfo(
                room_uuid=room.uuid,
                user_avatar_thumb=chat_image_url,
                user_id=last_message_user.id,
                user_name=chat_name,
                message=room.last_message_text,
                created=room.last_message_ts,
                have_unread_messages=room.have_unread_messages,
            )
        )

    return recents_data, next_page_cursor, previous_page_cursor


def get_or_create_room_by_company_and_members_ids(
    company_id: int, members_ids: List[int]
) -> Room:
    try:
        return room_providers.get_one_to_one_room_by_members_ids(
            company_id=company_id, members_ids=members_ids
        )
    except Room.DoesNotExist:
        pass

    channel = Room.objects.create(
        **{
            "company_id": company_id,
            "is_one_to_one": True,
            "name": str(uuid.uuid4()),
            "any_can_invite": False,
            "members_only": True,
            "max_users": 2,
        }
    )

    members = users_models.User.objects.filter(
        id__in=members_ids, company_id=company_id
    )

    if members.count() != len(members_ids):
        raise NonExistentMemberException("User does not exist")

    for member in members:
        channel.members.add(member)

    return channel


@cache(12 * 60 * 60)
def get_twilio_credentials_by_user_id(user_id: int) -> Dict[str, Any]:
    account_sid = settings.TWILIO_ACCOUNT_ID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    return client.tokens.create(ttl=60)


async def send_notification_chat_by_user_id_async(
    company_id: int, to_user_id: int, from_user_name: str, message: str
) -> None:
    payload = {"type": "notification", "ntype": "dm", "message": f"{message[:40]}..."}

    channel_name = user_services.get_user_notification_channel_by_user_id(
        company_id=company_id, user_id=to_user_id
    )
    await get_channel_layer().group_send(channel_name, payload)


def broadcast_chat_message_with_attachments(
    company_id: int,
    room_uuid: Union[str, uuid.UUID],
    message_uuid: Union[str, uuid.UUID],
) -> None:
    channel_layer = get_channel_layer()
    group = ROOM_GROUP_NAME.format(company_id=company_id, room_uuid=room_uuid)
    message = Message.objects.prefetch_related("attachments").get(uuid=message_uuid)

    serialized_message = _serialize_message(message)

    async_to_sync(channel_layer.group_send)(group, serialized_message)


def set_messages_readed_by_room_and_user(
    company_id: int, room_uuid: Union[str, UUID], user_id: int
) -> int:
    """
    Allow to mark unreaded messages readed by user in room
    Return the total messages marked as readed
    """
    return message_providers.set_messages_readed_by_room_and_user(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id
    )


def set_room_user_read(
    *, company_id: int, user_id: int, room_uuid: Union[str, uuid.UUID]
) -> None:
    """
    Set the RoomUserRead for and user and room
    """

    RoomUserRead.objects.update_or_create(
        company_id=company_id,
        user_id=user_id,
        room_uuid=room_uuid,
        defaults={"timestamp": timezone.now()},
    )


@database_sync_to_async
def update_room_last_message_by_room_uuid_async(
    *,
    company_id: int,
    user_id: int,
    room_uuid: Union[str, UUID],
    text: str,
    ts: datetime,
) -> int:
    return room_providers.update_room_last_message_by_room_uuid(
        company_id=company_id, user_id=user_id, room_uuid=room_uuid, text=text, ts=ts
    )


@database_sync_to_async
def send_message_to_devices_by_user_ids_async(
    company_id: int, room_uuid: Union[UUID, str], serialized_message: dict[str, Any]
) -> None:
    user_ids = set(
        Room.objects.get(uuid=room_uuid).members.values_list("id", flat=True)
    )
    devices_providers.send_message_to_devices_by_user_ids(
        company_id=company_id, user_ids=user_ids, serialized_message=serialized_message
    )
