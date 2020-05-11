import logging
from typing import Dict
from channels.db import database_sync_to_async
from django.core.cache import cache

from apps.core.uc import area_uc
from apps.core import models as core_models

logger = logging.getLogger(__name__)

USER_POSITION_KEY = "user-{}-position"


class GridMixin:
    @database_sync_to_async
    def save_position(self, area_id: int, x: int, y: int):
        area = core_models.Area.objects.get(id=area_id)
        uc = area_uc.SaveStateAreaUC(area)
        old_point = uc.execute(self.scope["user"], x, y)
        return old_point, uc.get_serialized_connected()

    @database_sync_to_async
    def clear_position(self, area_id: int, x: int, y: int):
        area = core_models.Area.objects.get(id=area_id)
        uc = area_uc.ClearStateAreaUC(area)
        uc.execute(self.scope["user"])

    async def grid_position(self, message):
        await self.send_json(message)

    async def grid_disconnect(self, message):
        await self.send_json(message)

    async def notify_change_position(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        logger.info("notify_change_position")
        logger.info(message)
        await self.channel_layer.group_send(self.company_channel, message)

    async def notify_user_disconnect(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        await self.channel_layer.group_send(self.company_channel, message)

    async def handle_grid_position(self, message: Dict) -> None:
        logger.info("handle_grid_position")
        logger.info(message)
        user = self.scope["user"]
        old_point, serialized_state = await self.save_position(
            message["area"], message["x"], message["y"]
        )
        message["old"] = old_point
        message["state"] = serialized_state
        cache.set(
            USER_POSITION_KEY.format(user.id),
            {"area_id": message["area"], "x": message["x"], "y": message["y"]},
        )
        await self.notify_change_position(message)

    async def handle_clear_user_position(self):
        """
            Executed when the user is disconnected
        """
        user = self.scope["user"]
        position: Dict = cache.get(USER_POSITION_KEY.format(user.id))
        if position:
            await self.clear_position(**position)
            await self.notify_user_disconnect(
                {"type": "grid.disconnect", **position}
            )
            cache.delete(USER_POSITION_KEY.format(user.id))
