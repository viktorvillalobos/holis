import json
from django.utils.translation import ugettext as _
import datetime as dt
from typing import Dict
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class NotificationMixin:
    async def notification(self, message: Dict) -> None:
        logger.info(message)
        await self.send_json(message)


class MainConsumer(NotificationMixin, AsyncJsonWebsocketConsumer):
    def get_groups(self):
        return ["adslab", "adslab_global"]

    async def connect_to_groups(self):
        for group in self.get_groups():
            await self.channel_layer.group_add(group, self.channel_name)

    async def connect(self):
        # Join room group
        await self.connect_to_groups()
        await self.accept()

    async def disconnect(self, close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

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

        if _type == "error":
            return await self.send_json({"error": _msg})
        elif _type == "chat.message":
            message: Dict = {
                "message": content["message"],
                "user": self.scope["user"].username,
            }
            return await self.notification(message)
        else:
            _msg = _("type not handled")
            return await self.send_json({"error": _msg})
