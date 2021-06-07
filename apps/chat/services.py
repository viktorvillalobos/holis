from typing import Any, Dict, List, Union

from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.query import Prefetch

import uuid
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from twilio.rest import Client

from apps.chat.lib.constants import ROOM_GROUP_NAME
from apps.users import models as users_models
from apps.users import services as user_services
from apps.utils.cache import cache

from ..chat import models as chat_models
from ..chat.api import serializers
from .providers import room as room_providers


class NonExistentMemberException(Exception):
    pass


@database_sync_to_async
def create_message_async(
    company_id: int, user_id: int, room_uuid: int, text: str
) -> chat_models.Message:
    return chat_models.Message.objects.create(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id, text=text
    )


def create_message(
    company_id: int, user_id: int, room_uuid: int, text: str
) -> chat_models.Message:
    return chat_models.Message.objects.create(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id, text=text
    )


def _serialize_message(message):
    data = serializers.MessageWithAttachmentsSerializer(message).data

    return {
        **data,
        **{"id": str(data["id"]), "room": str(data["room"]), "type": "chat.message"},
    }


@database_sync_to_async
def serialize_message(message: chat_models.Message) -> Dict[str, Any]:

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    return _serialize_message(message=message)


def get_recents_rooms(*, user_id: int, limit: int = 3) -> list[dict[str, Any]]:

    rooms_ids = (
        chat_models.Message.objects.filter(
            room__is_one_to_one=True, room__members__id=user_id
        )
        .order_by("room__uuid", "-created")
        .distinct("room__uuid")
        .values_list("room__uuid", flat=True)
    )[:limit]

    rooms = (
        chat_models.Room.objects.filter(uuid__in=rooms_ids)
        .order_by("created")
        .prefetch_related(
            Prefetch("members", queryset=users_models.User.objects.exclude(id=user_id))
        )
    )

    # rooms_data = (
    #     chat_models.Room.objects.filter(uuid__in=rooms_ids)
    #     .values("uuid", "members__avatar", "members__id", "members__name")
    #     .order_by("created")
    # )

    data = []

    for room in rooms:
        members = room.members.order_by("id")

        for member in members:
            data.append(
                {
                    "room": room.uuid,
                    "avatar_thumb": member.avatar_thumb,
                    "id": member.id,
                    "name": member.name,
                }
            )

    return data


def get_or_create_room_by_company_and_members_ids(
    company_id: int, members_ids: List[int]
) -> chat_models.Room:
    try:
        return room_providers.get_one_to_one_room_by_members_ids(
            company_id=company_id, members_ids=members_ids
        )
    except chat_models.Room.DoesNotExist:
        pass

    channel = chat_models.Room.objects.create(
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
    message = chat_models.Message.objects.prefetch_related("attachments").get(
        uuid=message_uuid
    )

    serialized_message = _serialize_message(message)

    async_to_sync(channel_layer.group_send)(group, serialized_message)
