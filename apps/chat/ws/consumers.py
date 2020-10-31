import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .utils import create_message, serialize_message

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

        _type = content["type"]

        logger.info(f"Chat type: {_type}")

        if _type == "echo":
            await self.chat_echo(content)
        elif _type == "chat.message":
            await self.broadcast_chat_message(content)
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

    async def broadcast_chat_message(self, content):
        assert isinstance(content["room"], str)
        assert isinstance(content["message"], str)
        logger.info("broadcast_chat_message")
        user = self.scope["user"]

        message = await create_message(user, content["room"], content["message"])
        serialized_message = await serialize_message(message)

        await self.channel_layer.group_send(self.room_group_name, serialized_message)

    async def chat_echo(self, event):
        logger.info("chat_echo")
        await self.send_json({"type": "chat.echo", "status": "ok"})

    async def chat_presence(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        await self.send_json(event)
