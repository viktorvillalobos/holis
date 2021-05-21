import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ..services import (
    create_message,
    send_notification_chat_by_user_id_async,
    serialize_message,
)

logger = logging.getLogger(__name__)
COMPANY_MAIN_CHANNEL = "company-chat-{}"


class ChatConsumer(AsyncJsonWebsocketConsumer):
    @property
    def room_name(self):
        try:
            return self.scope["url_route"]["kwargs"]["room_name"]
        except KeyError:
            raise Exception("CHAT: Error getting channel name from route")

    async def receive_json(self, content):

        user = self.scope["user"]
        _type = content["type"]
        is_one_to_one_chat = content.get("is_one_to_one")
        user_id = content.get("to")

        logger.info(f"Chat type: {_type}")

        if _type == "echo":
            await self.chat_echo(content)
        elif _type == "chat.message":
            await self.create_and_broadcast_message(content)

            if is_one_to_one_chat:

                logger.info(f"Is one-to-one chat sending notifications to {user_id}")
                await send_notification_chat_by_user_id_async(
                    company_id=user.company_id,
                    to_user_id=user_id,
                    from_user_name=user.name,
                    message=content["message"],
                )

        else:
            logger.info(f" {_type} type is not handled by ChatConsumer")

    async def connect(self):
        self.room_group_name = f"chat_{self.room_name}"
        logger.info(f"CONNECTING TO {self.room_group_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        _msg = {"type": "chat.presence", "kind": "connect", "user": "pepito"}
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        _msg = {"type": "chat.presence", "kind": "disconnect", "user": "pepito"}
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def create_and_broadcast_message(self, content):
        assert isinstance(content["room"], str)
        assert isinstance(content["message"], str)
        logger.info("broadcast_chat_message")
        user = self.scope["user"]

        message = await create_message(
            user.company_id, user.id, content["room"], content["message"]
        )
        serialized_message = await serialize_message(message=message)

        await self.channel_layer.group_send(self.room_group_name, serialized_message)

    async def chat_echo(self, event):
        logger.info("chat_echo")
        await self.send_json({"type": "chat.echo", "status": "ok"})

    async def chat_presence(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        await self.send_json(event)
