from typing import Dict

from django.conf import settings
from django.utils.translation import ugettext as _

import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.users.services import serialize_user

from .grid import GridMixin
from .notifications import NotificationMixin

logger = logging.getLogger(__name__)

COMPANY_MAIN_CHANNEL = "company-{}"


class MainConsumerBase(AsyncJsonWebsocketConsumer):
    @property
    def company_channel(self):
        company_id: int = self.scope["user"].company_id
        return COMPANY_MAIN_CHANNEL.format(company_id)

    async def get_groups(self):
        return [self.company_channel]

    @database_sync_to_async
    def serialize_user_data(self, user: settings.AUTH_USER_MODEL) -> Dict:
        return serialize_user(user)

    async def send_me_data(self):
        if self.scope["user"].id:
            await self.send_json(
                {
                    "type": "me.data",
                    "user": await self.serialize_user_data(self.scope["user"]),
                }
            )

    async def connect_to_groups(self):
        for group in await self.get_groups():
            await self.channel_layer.group_add(group, self.channel_name)


class MainConsumer(NotificationMixin, GridMixin, MainConsumerBase):
    async def receive_json(self, content):
        """
            This method receive jsons for clients, and
            distribute in diferent methods
        """
        try:
            _type = content["type"]
        except KeyError:
            _type = "error"
            _msg = _("Type is required")

        if _type == "error":
            return await self.send_json({"error": _msg})
        # elif _type == "chat.message":
        #     message: Dict = {
        #         "message": content["message"],
        #         "user": self.scope["user"].username,
        #     }
        #     return await self.notification(message)
        elif _type == "grid.position":
            await self.handle_grid_position(content)
        elif _type == "grid.clear":
            await self.handle_clear_user_position()
        elif _type == "grid.status":
            await self.handle_status(content)
        elif _type == "grid.heartbeat":
            await self.handle_heartbeat(content)
        elif _type == "grid.force.disconnect":
            await self.force_disconnect(content)
        else:
            _msg = _("type not handled by GridConsumer")
            return await self.send_json({"error": _msg})

    async def connect(self):
        # Join room group
        if self.scope["user"].is_authenticated:
            await self.connect_to_groups()
            await self.accept()

    async def disconnect(self, close_code):
        await self.handle_clear_user_position()

        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def force_disconnect(self, message):
        logger.info("force_disconnect")
        logger.info(message)
        user_id = message.get("user_id")
        if user_id:
            await self.handle_clear_user_position(user_id=user_id)
