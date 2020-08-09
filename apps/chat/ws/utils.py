from channels.db import database_sync_to_async
from apps.chat.uc.message import CreateMessage

from apps.chat import models as chat_models
from apps.users import models as user_models


@database_sync_to_async
async def create_message(
    user: user_models.User, room_id: str, text: str
) -> chat_models.Message:
    room = chat_models.Room.objects.get(id=room_id)
    uc = CreateMessage(room=room, user=user, text=text)
    uc.execute().get_message()
