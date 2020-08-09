from typing import Dict, Any, Optional
from channels.db import database_sync_to_async
from apps.chat.uc.message import CreateMessage

from apps.chat import models as chat_models
from apps.users import models as user_models
from apps.chat.api import serializers


@database_sync_to_async
def create_message(
    user: user_models.User, room_id: str, text: str
) -> chat_models.Message:
    room = chat_models.Room.objects.get(id=room_id)
    uc = CreateMessage(room=room, user=user, text=text)
    return uc.execute().get_message()


@database_sync_to_async
def serialize_message(message: chat_models.Message) -> Dict[str, Any]:

    data = serializers.MessageSerializer(message).data

    # This is a patch to Django Serializer BUG
    # https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable

    data["id"] = str(data["id"])
    data["room"] = str(data["room"])
    data["type"] = "chat.message"
    return data
