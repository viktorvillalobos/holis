import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


logger = logging.getLogger(__name__)
COMPANY_MAIN_CHANNEL = "company-chat-{}"


class ChatConsumer(AsyncJsonWebsocketConsumer):
    @property
    def room_name(self):
        try:
            return self.scope["url_route"]["kwargs"]["room_name"]
        except KeyError:
            raise Exception("CHAT: Error getting channel name from route")

    async def connect(self):
        self.room_group_name = f"chat_{self.room_name}"
        logger.info(f"CONNECTING TO {self.room_group_name}")

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        _msg = {"type": "chat.presence", "kind": "connect", "user": "pepito"}
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        _msg = {
            "type": "chat.presence",
            "kind": "disconnect",
            "user": "pepito",
        }
        await self.channel_layer.group_send(self.room_group_name, _msg)

    @property
    def events(self):
        return {
            "echo": self.chat_echo,
            "chat.message": self.broadcast_chat_message,
        }

    async def receive_json(self, content):

        _type = content["type"]

        logger.info(f"Chat type: {_type}")
        try:
            await self.events[_type](content)
        except KeyError:
            logger.info(f" {_type} type is not handled")

    async def broadcast_chat_message(self, content):
        logger.info("broadcast_chat_message")
        _msg = {
            "type": "chat.message",
            "message": content["message"],
            "user": {
                "name": self.scope["user"].name,
                "avatar": self.scope["user"].avatar_thumb
            }
        }
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def chat_echo(self, event):
        await self.send_json({"type": "chat.echo", "status": "ok"})

    async def chat_presence(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        await self.send_json(event)
