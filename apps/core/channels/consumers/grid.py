from typing import Dict, Optional, Tuple

from django.core.cache import cache

import datetime as dt
import logging
from channels.db import database_sync_to_async

from apps.users.models import User

from ... import services as core_services
from ...lib.dataclasses import PointData

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
        old_point = core_services.move_user_to_point_in_area_state_by_area_user_and_room(
            area_id=area_id,
            user=self.scope["user"],
            to_point_data=PointData(x, y),
            room=room,
        )
        return old_point.to_dict(), core_services.get_area_state(area_id)

    @database_sync_to_async
    def clear_position(
        self, area_id: int, x: int, y: int, room: str, timestamp: dt.datetime
    ):
        core_services.remove_user_from_area(area_id=area_id, user=self.scope["user"])
        return core_services.get_area_state(area_id=area_id)

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
        logger.info(f"HANDLE heartbeat {self.scope['user'].id}")
        logger.info(message)

        await self.heartbeat()
