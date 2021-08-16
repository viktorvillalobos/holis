from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.core.files.base import File
from django.utils import timezone

import uuid
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from datetime import datetime
from twilio.rest import Client
from uuid import UUID

from apps.users import services as user_services
from apps.users.context import models as users_models
from apps.users.lib.dataclasses import UserData
from apps.utils.cache import cache
from apps.utils.dataclasses import build_dataclass_from_model_instance

from ..chat.context.models import Message, Room, RoomUserRead
from .api.v100 import serializers as v100_serializers
from .context.providers import devices as devices_providers
from .context.providers import message as message_providers
from .context.providers import room as room_providers
from .lib.constants import ROOM_GROUP_NAME
from .lib.dataclasses import RecentRoomInfo, RoomData
from .lib.exceptions import NonExistentMemberException


@database_sync_to_async
def create_message_async(
    company_id: int,
    user_id: int,
    room_uuid: Union[UUID, str],
    text: str,
    app_uuid: Union[UUID, str],
) -> Message:
    return message_providers.create_message(
        company_id=company_id,
        room_uuid=room_uuid,
        user_id=user_id,
        text=text,
        app_uuid=app_uuid,
    )


def create_message(
    company_id: int, user_id: int, room_uuid: int, text: str, app_uuid: Union[UUID, str]
) -> Message:
    return message_providers.create_message(
        company_id=company_id,
        room_uuid=room_uuid,
        user_id=user_id,
        text=text,
        app_uuid=app_uuid,
    )


def _serialize_message(message, user):
    data = v100_serializers.MessageWithAttachmentsSerializer(
        message, context={"user": user}
    ).data

    return {
        **data,
        **{"id": str(data["id"]), "room": str(data["room"]), "type": "chat.message"},
    }


@database_sync_to_async
def serialize_message(message: Message, user: "User") -> Dict[str, Any]:

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    return _serialize_message(message=message, user=user)


def get_cursored_recents_rooms_by_user_id(
    *,
    company_id: int,
    user_id: int,
    is_one_to_one: bool = True,
    search: Optional[str] = None,
    cursor: Optional[dict[str, str]] = None,
    page_size: Optional[int] = 100,
    reverse: Optional[bool] = True,
) -> tuple[List[RecentRoomInfo], Optional[Dict[str, str]], Optional[Dict[str, str]]]:

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

        if is_one_to_one:
            other_user_id = [
                member_id for member_id in members_by_id.keys() if user_id != member_id
            ][0]
            chat_image_url = members_by_id[other_user_id].avatar_thumb
            chat_name = members_by_id[other_user_id].name
        else:
            raise NotImplementedError("We must implement grupal recents rooms")

        recents_data.append(
            RecentRoomInfo(
                uuid=room.uuid,
                image=chat_image_url,
                is_one_to_one=is_one_to_one,
                to_user_id=other_user_id,
                to_user_name=chat_name,
                last_message_text=room.last_message_text,
                last_message_ts=room.last_message_ts,
                last_message_user_id=room.last_message_user_id,
                have_unread_messages=room.have_unread_messages,
            )
        )

    return recents_data, next_page_cursor, previous_page_cursor


def get_or_create_one_to_one_room_by_company_and_users(
    company_id: int, to_user_id: int, from_user_id: int
) -> Room:
    room = room_providers.get_or_create_one_to_one_room_by_members_ids(
        company_id=company_id, from_user_id=from_user_id, to_user_id=to_user_id
    )

    members = users_models.User.objects.filter(
        id__in=[from_user_id, to_user_id], company_id=company_id
    )

    if members.count() != 2:
        raise NonExistentMemberException("User does not exist")

    room.members.set(members)
    return room


def create_many_to_many_room_by_name(
    company_id: int, members_ids: set[int], name: Optional[str] = "custom-room"
) -> Room:
    room = room_providers.create_many_to_many_room_by_name(
        company_id=company_id, name=name
    )

    members = users_models.User.objects.filter(
        id__in=members_ids, company_id=company_id
    )

    if members.count() != len(members_ids):
        raise NonExistentMemberException("User does not exist")

    room.members.set(members)
    return room


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
    user: "User",
) -> None:
    channel_layer = get_channel_layer()
    group = ROOM_GROUP_NAME.format(company_id=company_id, room_uuid=room_uuid)
    message = Message.objects.prefetch_related("attachments").get(uuid=message_uuid)

    serialized_message = _serialize_message(message, user=user)

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
    """
    Set the last message inside the room
    """
    return room_providers.update_room_last_message_by_room_uuid(
        company_id=company_id, user_id=user_id, room_uuid=room_uuid, text=text, ts=ts
    )


def send_message_to_devices_by_user_ids(
    company_id: int, room_uuid: Union[UUID, str], serialized_message: dict[str, Any]
) -> None:
    user_ids = Room.objects.get(uuid=room_uuid).members.values_list("id", flat=True)
    devices_providers.send_message_to_devices_by_user_ids(
        company_id=company_id, user_ids=user_ids, serialized_message=serialized_message
    )


def get_room_by_uuid(company_id: int, room_uuid: Union[UUID, str]) -> RoomData:
    """ Return a RoomData instance """
    room = room_providers.get_room_with_members_by_uuid(
        company_id=company_id, room_uuid=room_uuid
    )

    members = [
        build_dataclass_from_model_instance(klass=UserData, instance=member)
        for member in room.members.all()
    ]

    admins = [
        build_dataclass_from_model_instance(klass=UserData, instance=user)
        for user in room.admins.all()
    ]

    image_url = room.image.url if room.image else None

    return build_dataclass_from_model_instance(
        klass=RoomData,
        instance=room,
        members=members,
        admins=admins,
        image_url=image_url,
    )


def update_room_image_by_uuid(
    company_id: int, room_uuid: Union[UUID, str], image: File
) -> RoomData:
    room = room_providers.update_room_image_by_uuid(
        company_id=company_id, room_uuid=room_uuid, image=image
    )

    return build_dataclass_from_model_instance(klass=RoomData, instance=room)
