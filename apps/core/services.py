from typing import Any, Dict, List

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

import datetime
import itertools
import logging
from channels.db import database_sync_to_async
from datetime import timedelta

from apps.core.cachekeys import COMPANY_AREA_DATA_KEY
from apps.users import services as user_services
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .context.providers import area as area_providers
from .context.providers import presence as presence_providers
from .context.uc import area_uc
from .custom_types import AreaState
from .lib.constants import USER_POSITION_KEY
from .lib.dataclasses import AreaData, AreaItem, MovementData, PointData

logger = logging.getLogger(__name__)


def get_area(area_id: int) -> AreaData:
    area = area_providers.get_area_instance_by_id(area_id=area_id)

    return build_dataclass_from_model_instance(klass=AreaData, instance=area)


def get_area_items_for_connected_users_by_id(area_id: int) -> List[Dict[str, Any]]:
    return area_uc.get_area_items_for_connected_users_by_id(area_id=area_id)


def move_user_to_point_in_area_state_by_area_user_and_room(
    area_id: int, user: settings.AUTH_USER_MODEL, to_point_data: PointData, room: str
) -> PointData:
    movement_data = area_uc.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area_id, user=user, to_point_data=to_point_data, room=room
    )

    return movement_data.from_point


def remove_user_from_area_by_area_and_user_id(
    area_id: int, user_id: int, serialize=False
) -> List[Dict[str, Any]]:
    """
    Disconnect and user and later remove the user
    from the state and return the new state
    """
    user_services.disconnect_user_by_id(user_id=user_id)

    return area_uc.remove_user_from_area_by_area_and_user_id(
        area_id=area_id, user_id=user_id, serialize=serialize
    )


def get_connected_user_from_company_areas_from_cache(company_id: int):
    areas = area_providers.get_company_areas_by_company_id(company_id=company_id)
    area_states_keys = cache.keys(
        COMPANY_AREA_DATA_KEY.format(company_id=company_id, area_id="*")
    )

    if not area_states_keys:
        areas = area_providers.get_company_areas_by_company_id(company_id=company_id)
        return [
            {"company_id": company_id, "id": area.id, "state": []} for area in areas
        ]

    area_states = cache.get_many(area_states_keys)

    response = []
    for key, area_state in area_states.items():
        _, _, _, area_id, _ = key.split("-")
        serialized_state = [
            [item.to_dict() for item in row if item.id]
            for row in area_state
            if len(row)
        ]
        serialized_state = list(itertools.chain(*serialized_state))

        response.append(
            {"company_id": company_id, "id": int(area_id), "state": serialized_state}
        )

    return response


def get_users_connecteds_by_area_from_cache(company_id: int):
    """
    Return the list of connected users by area, if there is any user
    connected, return the list of area with empty state
    """
    connected_users_keys = cache.keys(USER_POSITION_KEY.format(company_id, "*"))

    if not connected_users_keys:
        areas = area_providers.get_company_areas_by_company_id(company_id=company_id)
        return [
            {"company_id": company_id, "id": area.id, "state": []} for area in areas
        ]

    user_position_values = cache.get_many(connected_users_keys).values()

    an_iterator = itertools.groupby(user_position_values, lambda x: x["area_id"])

    return [
        {"company_id": company_id, "id": key, "state": list(group)}
        for key, group in an_iterator
    ]


@database_sync_to_async
def set_cached_position(
    company_id: int, area: int, user: "User", x: int, y: int, room: str
) -> None:
    logger.info(f"SET CACHED POSITION FOR USER {user.id} in AREA {area}")
    timestamp = timezone.now()

    area_item = AreaItem.from_user(
        user=user, area_id=area, x=x, y=y, room=room, last_seen=timestamp
    )

    cache_key = USER_POSITION_KEY.format(company_id, user.id)
    logger.info(f"user position key: {cache_key}")
    cache.set(cache_key, area_item)


def get_cached_position(company_id: int, user_id: int) -> Dict[str, Any]:
    return area_uc.get_cached_position(company_id=company_id, user_id=user_id)


def delete_cached_position(company_id: int, user_id: int) -> None:
    key = USER_POSITION_KEY.format(company_id, user_id)
    cache.delete(key)


def get_disconnected_users_ids_by_company_id(company_id: int) -> list[tuple[int, int]]:
    """
    Return a list of tuples with tuple([users, area_id]) without healtcheck about 60 seconds ago.
    """

    one_minute_ago = timezone.now() - timedelta(seconds=60)

    user_position_positions_values = presence_providers.get_disconnect_users_ids_by_company_id(
        company_id=company_id
    )

    to_disconnect_user_ids = []
    for key, value in user_position_positions_values.items():
        last_seen = datetime.datetime.fromisoformat(value["last_seen"])
        if last_seen < one_minute_ago:
            _, _, _, user_id, _ = key.split("-")
            to_disconnect_user_ids.append((int(user_id), value["area_id"]))

    return to_disconnect_user_ids
