from typing import Any, Dict, Optional, Tuple

from django.core.cache import cache

import datetime as dt
import logging
from channels.db import database_sync_to_async

from apps.users.models import User
from apps.users.services import serialize_user

from ... import services as core_services
from ...lib.dataclasses import PointData

logger = logging.getLogger(__name__)

USER_POSITION_KEY = "user-{}-position"


def set_cached_position(area: int, user_id: int, x: int, y: int, room: str) -> None:
    cache.set(
        USER_POSITION_KEY.format(user_id),
        {
            "area_id": area,
            "x": x,
            "y": y,
            "room": room,
            "timestamp": str(dt.datetime.now()),
        },
    )


def get_cached_position(user_id: int) -> Dict[str, Any]:
    key = USER_POSITION_KEY.format(user_id)
    return cache.get(key)


def delete_cached_position(user_id: int) -> None:
    key = USER_POSITION_KEY.format(user_id)
    cache.delete(key)


@database_sync_to_async
def execute_heartbeat(user: "User", area_id: int = None) -> None:
    user.touch(area_id=area_id)


@database_sync_to_async
def get_user_by_user_id(user_id):
    return User.objects.get(id=user_id)


@database_sync_to_async
def save_position(
    user: "User", area: int, x: int, y: int, room: Optional[str] = None
) -> Tuple[PointData, Dict[str, Any]]:

    execute_heartbeat(user=user, area_id=area)

    old_point = core_services.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area, user=user, to_point_data=PointData(x, y), room=room
    )

    return (
        old_point,
        core_services.get_area_items_for_connected_users_by_id(area_id=area),
    )


async def notify_user_disconnect(channel_layer, company_channel, user, message):
    message["user"] = await database_sync_to_async(serialize_user)(user)
    await channel_layer.group_send(company_channel, message)


async def handle_clear_user_position(channel_layer, company_channel, user: "User"):
    """
    Executed when the user is disconnected
    """
    cached_position = get_cached_position(user_id=user.id)

    if cached_position:
        state = await database_sync_to_async(
            core_services.remove_user_from_area_by_area_and_user_id
        )(area_id=cached_position["area_id"], user=user)

        await notify_user_disconnect(
            channel_layer=channel_layer,
            company_channel=company_channel,
            user=user,
            message={"type": "grid.disconnect", "state": state, **cached_position},
        )
        delete_cached_position(user_id=user.id)


async def notify_change_position(channel_layer, company_channel, user, message):
    message["user"] = await database_sync_to_async(serialize_user)(user)
    await channel_layer.group_send(company_channel, message)


async def handle_grid_position(
    channel_layer, company_channel, user: "User", message: Dict[str, Any]
) -> None:
    to_be_save_data_position = {"user": user, **message}
    to_be_save_data_position.pop("type")

    to_be_cached_position = {"user_id": user.id, **message}
    to_be_cached_position.pop("type")

    set_cached_position(**to_be_cached_position)

    old_point_data, serialized_state = await save_position(**to_be_save_data_position)

    await notify_change_position(
        channel_layer=channel_layer,
        company_channel=company_channel,
        user=user,
        message={"old": old_point_data.to_dict(), "state": serialized_state, **message},
    )


async def handle_force_disconnect(channel_layer, company_channel, message):
    user_id = message.get("user_id")

    if user_id:
        await handle_clear_user_position(
            channel_layer=channel_layer,
            company_channel=company_channel,
            user_id=user_id,
        )


async def handle_notify_user_status(
    channel_layer, company_channel, user, message
) -> None:
    message["user"] = database_sync_to_async(serialize_user)(user)
    await channel_layer.group_send(company_channel, message)