import datetime as dt
import logging
from typing import Dict, Optional, Tuple

from channels.db import database_sync_to_async
from django.core.cache import cache

from apps.core import models as core_models
from apps.core.uc import area_uc
from apps.users.models import User

from ...entities import Point
from ...services import add_user_to_area, get_area_state, remove_user_from_area

logger = logging.getLogger(__name__)

USER_POSITION_KEY = "user-{}-position"


class GridMixin:
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def heartbeat(self):
        self.scope["user"].touch()

    @database_sync_to_async
    def save_position(
        self, area_id: int, x: int, y: int, room: Optional[str] = None
    ) -> Tuple[Tuple, Dict]:
        self.scope["user"].touch(area_id=area_id)
        old_point = add_user_to_area(area_id, self.scope["user"], Point(x, y), room)
        return old_point.to_dict(), get_area_state(area_id)

    @database_sync_to_async
    def clear_position(
        self, area_id: int, x: int, y: int, room: str, timestamp: dt.datetime
    ):
        remove_user_from_area(area_id, self.scope["user"])
        return get_area_state(area_id)

    async def grid_position(self, message):
        await self.send_json(message)

    async def grid_disconnect(self, message):
        await self.send_json(message)

    async def grid_status(self, message):
        await self.send_json(message)

    async def notify_change_position(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        await self.channel_layer.group_send(self.company_channel, message)

    async def notify_user_disconnect(self, message, user_id=None):

        if user_id:
            user = await self.get_user(user_id)
        else:
            user = self.scope["user"]
        message["user"] = await self.serialize_user_data(user)
        await self.channel_layer.group_send(self.company_channel, message)

    async def notify_user_status(self, message):
        message["user"] = await self.serialize_user_data(self.scope["user"])
        await self.channel_layer.group_send(self.company_channel, message)

    async def handle_grid_position(self, message: Dict) -> None:
        user = self.scope["user"]
        area: int = message["area"]
        x: int = message["x"]
        y: int = message["y"]
        room: int = message["room"]
        old_point, serialized_state = await self.save_position(area, x, y, room)
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

    async def handle_clear_user_position(self, user_id=None):
        """
            Executed when the user is disconnected
        """
        logger.info("HANDLE CLEAR USER POSITION")
        user_id = user_id or self.scope["user"].id
        logger.info(user_id)
        key = USER_POSITION_KEY.format(user_id)
        position: Dict = cache.get(key)
        logger.info("POSITION")
        logger.info(position)
        if position:

            state = await self.clear_position(**position)
            await self.notify_user_disconnect(
                {"type": "grid.disconnect", "state": state, **position}, user_id
            )
            cache.delete(USER_POSITION_KEY.format(user_id))

    async def handle_status(self, message):
        logger.info("HANDLE STATUS")
        logger.info(message)

        await self.notify_user_status(message)

    async def handle_heartbeat(self, message):
        logger.info("HANDLE heartbeat")
        logger.info(message)

        await self.heartbeat()
