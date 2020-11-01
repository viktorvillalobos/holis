from typing import Any, Dict

from django.core.files.storage import default_storage
from channels.db import database_sync_to_async

from ..chat import models as chat_models
from ..chat.api import serializers


@database_sync_to_async
def create_message(
    company_id: int, user_id: int, room_id: int, text: str
) -> chat_models.Message:
    return chat_models.Message.objects.create(
        company_id=company_id, room_id=room_id, user_id=user_id, text=text
    )


@database_sync_to_async
def serialize_message(message: chat_models.Message) -> Dict[str, Any]:

    data = serializers.MessageSerializer(message).data

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    data["id"] = str(data["id"])
    data["room"] = str(data["room"])
    data["type"] = "chat.message"
    return data


def get_recents_rooms(user_id: id) -> Dict[str, Any]:
    rooms_ids = (
        chat_models.Message.objects.filter(
            room__is_one_to_one=True, room__members__id=user_id,
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