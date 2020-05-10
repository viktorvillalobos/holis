import logging
from typing import Dict
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.translation import ugettext as _

from apps.users.api.serializers import UserSerializer

from .grid import GridMixin
from .notifications import NotificationMixin

logger = logging.getLogger(__name__)


class MainConsumerBase(AsyncJsonWebsocketConsumer):
    async def get_groups(self):
        return ["adslab"]

    @database_sync_to_async
    def serialize_user_data(self, user):
        return UserSerializer(user).data

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
        logger.info(content)
        try:
            _type = content["type"]
        except KeyError:
            _type = "error"
            _msg = _("Type is required")

        logger.info(_type)

        if _type == "error":
            return await self.send_json({"error": _msg})
        elif _type == "chat.message":
            message: Dict = {
                "message": content["message"],
                "user": self.scope["user"].username,
            }
            return await self.notification(message)
        elif _type == "grid.position":
            logger.info("handling grid position")
            await self.handle_grid_position(content)
        else:
            _msg = _("type not handled")
            return await self.send_json({"error": _msg})

    async def connect(self):
        # Join room group
        await self.connect_to_groups()
        await self.accept()
        await self.send_me_data()

    async def disconnect(self, close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

        await self.handle_clear_user_position()
