from typing import Any, Dict, List

from django.conf import settings
from django.core.files.storage import default_storage

import uuid
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from twilio.rest import Client

from apps.users import models as users_models
from apps.users import services as user_services
from apps.utils.cache import cache

from ..chat import models as chat_models
from ..chat.api import serializers
from .providers import room as room_providers


class NonExistentMemberException(Exception):
    pass


@database_sync_to_async
def create_message(
    company_id: int, user_id: int, room_id: int, text: str
) -> chat_models.Message:
    return chat_models.Message.objects.create(
        company_id=company_id, room_id=room_id, user_id=user_id, text=text
    )


@database_sync_to_async
def serialize_message(message: chat_models.Message) -> Dict[str, Any]:

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    data = serializers.MessageRawSerializer(message).data

    return {
        **data,
        **{"id": str(data["id"]), "room": str(data["room"]), "type": "chat.message"},
    }


def get_recents_rooms(user_id: id) -> Dict[str, Any]:
    rooms_ids = (
        chat_models.Message.objects.filter(
            room__is_one_to_one=True, room__members__id=user_id
        )
        .order_by("room__id", "-created")
        .distinct("room__id")
        .values_list("room__id", flat=True)
    )[:3]

    rooms_data = (
        chat_models.Room.objects.filter(id__in=rooms_ids)
        .prefetch_related("members")
        .values("id", "members__avatar", "members__id", "members__name")
    )

    return [
        {
            "room": x["id"],
            "avatar_thumb": default_storage.url(x["members__avatar"]),
            "id": x["members__id"],
            "name": x["members__name"],
        }
        for x in rooms_data
        if x["members__id"] != user_id
    ]


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
    to_user_id: int, from_user_name: str, message: str
) -> None:
    payload = {"type": "notification", "ntype": "dm", "message": f"{message[:40]}..."}

    channel_name = user_services.get_user_notification_channel_by_user_id(
        user_id=to_user_id
    )
    await get_channel_layer().group_send(channel_name, payload)
