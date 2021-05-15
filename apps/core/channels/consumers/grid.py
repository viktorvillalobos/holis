from typing import Any, Dict, List, Optional, Tuple

from django.core.cache import cache
from django.utils import timezone

import datetime as dt
import logging
from channels.db import database_sync_to_async

from apps.core.custom_types import AreaState
from apps.users import services as user_services
from apps.users.models import User

from ... import services as core_services
from ...lib.constants import USER_POSITION_KEY
from ...lib.dataclasses import AreaItem, PointData

logger = logging.getLogger(__name__)


def set_cached_position(
    company_id: int, area: int, user: "User", x: int, y: int, room: str
) -> None:
    logger.info(f"SET CACHED POSITION FOR USER {user.id} in AREA {area}")
    timestamp = timezone.now()

    to_be_cached_area_item_data = AreaItem.from_user(
        user=user, area_id=area, x=x, y=y, room=room, last_seen=timestamp
    ).to_dict()

    cache.set(
        USER_POSITION_KEY.format(company_id, user.id), to_be_cached_area_item_data
    )


def get_cached_position(company_id: int, user_id: int) -> Dict[str, Any]:
    key = USER_POSITION_KEY.format(company_id, user_id)
    return cache.get(key)


def delete_cached_position(company_id: int, user_id: int) -> None:
    key = USER_POSITION_KEY.format(company_id, user_id)
    cache.delete(key)


@database_sync_to_async
def get_user_by_user_id(user_id):
    return User.objects.get(id=user_id)


@database_sync_to_async
def execute_heartbeat(user: "User", area_id: int = None) -> None:
    logger.info(f"Touch: {user}")
    user_services.touch_user_by_user_and_area_id(user_id=user.id, area_id=area_id)


@database_sync_to_async
def save_position(
    user: "User", area: int, x: int, y: int, room: Optional[str] = None
) -> Tuple[PointData, List[Dict[str, Any]]]:
    # TODO: rename area to area_id

    user_services.touch_user_by_user_and_area_id(user_id=user.id, area_id=area)

    old_point = core_services.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area, user=user, to_point_data=PointData(x, y), room=room
    )

    return (
        old_point,
        core_services.get_area_items_for_connected_users_by_id(area_id=area),
    )


async def notify_user_disconnect(channel_layer, company_channel, user, message):
    message["user"] = await database_sync_to_async(user_services.serialize_user)(user)
    await channel_layer.group_send(company_channel, message)


async def handle_clear_user_position(channel_layer, company_channel, user: "User"):
    """
    Executed when the user is disconnected
    """
    logger.info("core.channels.consumers.grid.handle_clear_user_position")
    last_user_position = get_cached_position(
        company_id=user.company_id, user_id=user.id
    )
    last_user_position["timestamp"] = last_user_position["timestamp"].isoformat()

    if last_user_position:
        logger.info("User in cached position, proceed to remove")
        state = await database_sync_to_async(
            core_services.remove_user_from_area_by_area_and_user_id
        )(area_id=last_user_position["area_id"], user_id=user.id)

        delete_cached_position(company_id=user.company_id, user_id=user.id)

        await notify_user_disconnect(
            channel_layer=channel_layer,
            company_channel=company_channel,
            user=user,
            message={"type": "grid.disconnect", "state": state, **last_user_position},
        )
    else:
        logger.info("User without cached position")


async def notify_change_position(channel_layer, company_channel, user, message):
    message["user"] = await database_sync_to_async(user_services.serialize_user)(user)
    await channel_layer.group_send(company_channel, message)


async def handle_user_movement(
    channel_layer, company_channel, user: "User", message: Dict[str, Any]
) -> None:
    logger.info(f"handle_user_movement of user {user.id}")
    to_be_save_data_position = {"user": user, **message}
    to_be_save_data_position.pop("type")

    to_be_cached_position = {"company_id": user.company_id, "user": user, **message}
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
        user = await get_user_by_user_id(user_id=user_id)
        await handle_clear_user_position(
            channel_layer=channel_layer, company_channel=company_channel, user=user
        )


async def handle_notify_user_status(
    channel_layer, company_channel, user, message
) -> None:
    message["user"] = database_sync_to_async(user_services.serialize_user)(user)
    await channel_layer.group_send(company_channel, message)
