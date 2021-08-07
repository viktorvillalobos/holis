import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.chat.lib.constants import ROOM_GROUP_NAME

from .. import services as chat_services
from .. import tasks as chat_tasks

logger = logging.getLogger(__name__)
COMPANY_MAIN_CHANNEL = "company-chat-{}"


class ChatConsumer(AsyncJsonWebsocketConsumer):
    @property
    def room_uuid(self):
        try:
            return self.scope["url_route"]["kwargs"]["room_uuid"]
        except KeyError:
            raise Exception("CHAT: Error getting channel name from route")

    async def receive_json(self, message):

        user = self.scope["user"]
        _type = message["type"]
        is_one_to_one_chat = message.get("is_one_to_one")
        user_id = message.get("to")

        logger.info(f"Chat type: {_type}")

        if _type == "echo":
            await self.chat_echo(message)
        elif _type == "chat.message":
            await self.create_and_broadcast_message(message)

            if is_one_to_one_chat:

                logger.info(f"Is one-to-one chat sending notifications to {user_id}")
                await chat_services.send_notification_chat_by_user_id_async(
                    company_id=user.company_id,
                    to_user_id=user_id,
                    from_user_name=user.name,
                    message=message["message"],
                )
        else:
            logger.info(f" {_type} type is not handled by ChatConsumer")

    async def connect(self):
        self.room_group_name = ROOM_GROUP_NAME.format(
            company_id=self.scope["user"].company_id, room_uuid=self.room_uuid
        )
        logger.info(f"CONNECTING TO {self.room_group_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        _msg = {"type": "chat.presence", "kind": "connect", "user": "pepito"}
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        _msg = {"type": "chat.presence", "kind": "disconnect", "user": "pepito"}
        await self.channel_layer.group_send(self.room_group_name, _msg)

    async def create_and_broadcast_message(self, message):
        assert isinstance(message["room"], str)
        assert isinstance(message["message"], str)
        logger.info("broadcast_chat_message")
        user = self.scope["user"]

        message = await chat_services.create_message_async(
            company_id=user.company_id,
            user_id=user.id,
            room_uuid=message["room"],
            text=message["message"],
            app_uuid=message["app_uuid"],
        )
        serialized_message = await chat_services.serialize_message(
            message=message, user=user
        )
        await self.channel_layer.group_send(self.room_group_name, serialized_message)

        # TODO: This needs debounce
        await chat_tasks.send_message_to_devices_by_user_ids_task_async(
            company_id=user.company_id,
            room_uuid=message.room_uuid,
            serialized_message=serialized_message,
        )

        await chat_services.update_room_last_message_by_room_uuid_async(
            company_id=user.company_id,
            room_uuid=message.room_uuid,
            ts=message.created,
            text=message.text,
            user_id=message.user_id,
        )

    async def chat_echo(self, event):
        logger.info("chat_echo")
        await self.send_json({"type": "chat.echo", "status": "ok"})

    async def chat_presence(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        await self.send_json(event)
