from typing import Any, Dict, List, Union

from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.query import Prefetch

import uuid
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from datetime import datetime
from twilio.rest import Client
from uuid import UUID

from apps.chat.lib.constants import ROOM_GROUP_NAME
from apps.users import models as users_models
from apps.users import services as user_services
from apps.utils.cache import cache

from ..chat.api import serializers
from ..chat.models import Message, Room
from .providers import message as message_providers
from .providers import room as room_providers


class NonExistentMemberException(Exception):
    pass


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


def get_recents_rooms_by_user_id(
    *, user_id: int, is_one_to_one: bool = True, limit: int = 3
) -> list[dict[str, Any]]:

    recents_messages = list(
        message_providers.get_recents_messages_by_user_id(
            user_id=user_id, is_one_to_one=is_one_to_one, limit=limit
        )
    )

    recents_messages = sorted(recents_messages, key=lambda x: x.created, reverse=True)

    recent_messages_by_room = {
        message.room_uuid: message for message in recents_messages
    }

    rooms_in_bulk = room_providers.get_rooms_by_uuids_in_bulk(
        room_uuids=recent_messages_by_room.keys()
    )

    recents_data = []
    for room_uuid in recent_messages_by_room.keys():

        last_room_message = recent_messages_by_room[room_uuid]
        room = rooms_in_bulk[room_uuid]
        users = room.members.exclude(id=user_id).order_by("id")

        assert users.count() == 1

        for member in users:
            recents_data.append(
                {
                    "room": room_uuid,
                    "avatar_thumb": member.avatar_thumb,
                    "id": member.id,
                    "name": member.name,
                    "message": last_room_message.text,
                    "created": last_room_message.created,
                    "have_unread_messages": last_room_message.have_unread_messages,
                }
            )

    return recents_data


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


@database_sync_to_async
def set_messages_readed_by_room_and_user_async(
    company_id: int, room_uuid: Union[str, UUID], user_id: int
) -> int:
    """ Allow to mark unreaded messages readed by user in room """
    return message_providers.set_messages_readed_by_room_and_user(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id
    )
