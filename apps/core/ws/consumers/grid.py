import datetime as dt
import logging
from typing import Dict, Optional, Tuple

from apps.core import models as core_models
from apps.core.uc import area_uc
from channels.db import database_sync_to_async
from django.core.cache import cache

logger = logging.getLogger(__name__)

USER_POSITION_KEY = "user-{}-position"


class GridMixin:
    @database_sync_to_async
    def save_position(
        self, area_id: int, x: int, y: int, room: Optional[str] = None
    ) -> Tuple[Tuple, Dict]:
        area = core_models.Area.objects.get(id=area_id)
        uc = area_uc.SaveStateAreaUC(area)
        old_point = uc.execute(self.scope["user"], x, y, room)
        return old_point, uc.get_serialized_connected()

    @database_sync_to_async
    def clear_position(
        self, area_id: int, x: int, y: int, room: str, timestamp: dt.datetime
    ):
        area = core_models.Area.objects.get(id=area_id)
        uc = area_uc.ClearStateAreaUC(area)
        uc.execute(self.scope["user"])
        return uc.get_serialized_connected()

    async def grid_position(self, message):
        await self.send_json(message)

    async def grid_disconnect(self, message):
        await self.send_json(message)

    async def notify_change_position(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        await self.channel_layer.group_send(self.company_channel, message)

    async def notify_user_disconnect(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        await self.channel_layer.group_send(self.company_channel, message)

    async def handle_grid_position(self, message: Dict) -> None:
        user = self.scope["user"]
        area: int = message["area"]
        x: int = message["x"]
        y: int = message["y"]
        room: int = message["room"]
        old_point, serialized_state = await self.save_position(
            area, x, y, room
        )
        message["old"] = old_point
        message["state"] = serialized_state
        cache.set(
            USER_POSITION_KEY.format(user.id),
            {
                "area_id": area,
                "x": x,
                "y": y,
                "room": room,
                "timestamp": str(dt.datetime.now()),
            },
        )
        await self.notify_change_position(message)

    async def handle_clear_user_position(self):
        """
            Executed when the user is disconnected
        """
        user = self.scope["user"]
        key = USER_POSITION_KEY.format(user.id)
        position: Dict = cache.get(key)
        if position:

            state = await self.clear_position(**position)
            await self.notify_user_disconnect(
                {"type": "grid.disconnect", "state": state, **position}
            )
            cache.delete(USER_POSITION_KEY.format(user.id))
