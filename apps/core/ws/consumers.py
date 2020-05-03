import logging
from typing import Dict
from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.translation import ugettext as _

from apps.users.api.serializers import UserSerializer
from apps.core.uc import area_uc
from apps.core import models as core_models

logger = logging.getLogger(__name__)


class NotificationMixin:
    async def notification(self, message: Dict) -> None:
        logger.info(message)
        await self.send_json(message)


class GridMixin:
    @database_sync_to_async
    def save_position(self, area_id: int, x: int, y: int):
        area = core_models.Area.objects.get(id=area_id)
        uc = area_uc.SaveStateAreaUC(area)
        positions = uc.execute(self.scope["user"], x, y)
        return {
            "positions": positions,
            "state": uc.get_serialized_connected()
        }

    async def grid_position(self, message):
        await self.send_json(message)

    async def notify_change_position(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        logger.info("notify_change_position")
        logger.info(message)
        await self.channel_layer.group_send("adslab", message)

    async def handle_grid_position(self, message: Dict) -> None:
        logger.info("handle_grid_position")
        logger.info(message)
        results = await self.save_position(message["area"], message["x"], message["y"])
        message["old"] = results["positions"]
        message["state"] = results["state"]
        await self.notify_change_position(message)


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

    async def connect(self):
        # Join room group
        await self.connect_to_groups()
        await self.accept()
        await self.send_me_data()

    async def disconnect(self, close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)


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
