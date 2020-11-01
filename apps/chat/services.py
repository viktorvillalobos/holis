from typing import Any, Dict

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
