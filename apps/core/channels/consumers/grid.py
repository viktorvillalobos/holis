from typing import Any, Dict, Optional, Tuple

from django.core.cache import cache

import datetime as dt
import logging
from channels.db import database_sync_to_async

from apps.users.models import User

from ... import services as core_services
from ...lib.dataclasses import PointData

logger = logging.getLogger(__name__)

USER_POSITION_KEY = "user-{}-position"


def _set_cached_position(area_id: int, user_id: int, x: int, y: int, room: str) -> None:
    cache.set(
        USER_POSITION_KEY.format(user_id),
        {
            "area_id": area_id,
            "x": x,
            "y": y,
            "room": room,
            "timestamp": str(dt.datetime.now()),
        },
    )


def _get_cached_position(user_id: int) -> Dict[str, Any]:
    key = USER_POSITION_KEY.format(user_id)
    return cache.get(key)


def _delete_cached_position(user_id: int) -> None:
    key = USER_POSITION_KEY.format(user_id)
    cache.delete(key)


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
        return (
            old_point.to_dict(),
            core_services.get_area_items_for_connected_users_by_id(area_id=area_id),
        )

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

    async def handle_grid_position(self, message: Dict[str, Any]) -> None:
        user = self.scope["user"]
        area_id: int = message["area"]
        x: int = message["x"]
        y: int = message["y"]
        room: int = message["room"]
        old_point, serialized_state = await self.save_position(area_id, x, y, room)
        message["old"] = old_point
        message["state"] = serialized_state
        _set_cached_position(area_id=area_id, user_id=user.id, x=x, y=y, room=room)
        await self.notify_change_position(message)

    async def handle_clear_user_position(self, user_id=None):
        """
        Executed when the user is disconnected
        """
        user_id = user_id or self.scope["user"].id

        cached_position = _get_cached_position(user_id=user_id)

        if cached_position:
            state = await database_sync_to_async(
                core_services.remove_user_from_area_by_area_and_user_id
            )(area_id=cached_position["area_id"], user=self.scope["user"])

            await self.notify_user_disconnect(
                {"type": "grid.disconnect", "state": state, **cached_position}, user_id
            )
            _delete_cached_position(user_id=user_id)

    async def handle_status(self, message):
        await self.notify_user_status(message)

    async def handle_heartbeat(self, message):
        await self.heartbeat()
