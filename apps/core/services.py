from typing import Any, Dict, List

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

import itertools
import logging
from datetime import timedelta

from apps.core.uc import area_uc
from apps.users import services as user_services
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .custom_types import AreaState
from .lib.constants import USER_POSITION_KEY
from .lib.dataclasses import AreaData, AreaItem, MovementData, PointData
from .providers import area as area_providers

logger = logging.getLogger(__name__)


def get_area(area_id: int) -> AreaData:
    area = area_providers.get_area_instance_by_id(area_id=area_id)

    return build_dataclass_from_model_instance(klass=AreaData, instance=area)


def get_area_items_for_connected_users_by_id(area_id: int) -> List[Dict[str, Any]]:
    return area_uc.get_area_items_for_connected_users_by_id(area_id=area_id)


def move_user_to_point_in_area_state_by_area_user_and_room(
    area_id: int, user: settings.AUTH_USER_MODEL, to_point_data: PointData, room: str
) -> MovementData:
    return area_uc.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area_id, user=user, to_point_data=to_point_data, room=room
    )


def remove_user_from_area_by_area_and_user_id(
    area_id: int, user_id: int
) -> List[Dict[str, Any]]:
    """
    Disconnect and user and later remove the user
    from the state and return the new state
    """
    user_services.disconnect_user_by_id(user_id=user_id)

    return area_uc.remove_user_from_area_by_area_and_user_id(
        area_id=area_id, user_id=user_id
    )


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
