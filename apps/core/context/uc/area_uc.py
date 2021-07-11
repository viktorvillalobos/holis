"""
    UseCases for Area
"""
from typing import Any, Dict, List, Tuple

from django.core.cache import cache

import logging

from apps.users.context.models import User

from ...cachekeys import COMPANY_AREA_DATA_KEY
from ...custom_types import AreaState
from ...lib.dataclasses import AreaItem, MovementData, PointData
from ..models import Area
from ..providers import area as area_providers

logger = logging.getLogger(__name__)


class UserNotFoundInStateException(Exception):
    pass


def _serialize_and_commit_area_state(area: Area, area_state: AreaState) -> Area:
    key = COMPANY_AREA_DATA_KEY.format(company_id=area.company_id, area_id=area.id)
    cache.set(key, area_state)
    return area


def _create_empty_area_by_width_and_height(
    area_id: int, width: int, height: int
) -> list[list[AreaItem]]:
    return [
        [AreaItem.zero(area_id=area_id) for x in range(width)] for x in range(height)
    ]


def _get_or_create_area_state_by_area_id(
    area_id: int,
) -> Tuple[List[List[AreaItem]], Area, bool]:
    area = area_providers.get_area_instance_by_id(area_id=area_id)
    area_key = COMPANY_AREA_DATA_KEY.format(company_id=area.company_id, area_id=area.id)
    area_state = cache.get(area_key)

    if not area_state:
        area_state = _create_empty_area_by_width_and_height(
            area_id=area.id, width=area.width, height=area.height
        )
        area = _serialize_and_commit_area_state(area=area, area_state=area_state)
        return area_state, area, True

    return (area_state, area, False)


def _get_connected_ids_in_area_state_by_state(area_state: AreaState):
    state_connected_ids = []
    for row in area_state:
        state_connected_ids += [area_item for area_item in row if area_item.id != 0]

    return state_connected_ids


def _get_user_state_point_position_by_user_id(
    area_state: AreaState, user_id: int
) -> PointData:
    logger.info("get_user_position")
    x_pos = 0
    y_pos = 0

    try:
        for x, row in enumerate(area_state):
            for y, column in enumerate(row):
                if user_id == column.id:
                    x_pos = x
                    y_pos = y
                    break
    except IndexError:
        raise UserNotFoundInStateException

    return PointData(x=x_pos, y=y_pos)


def _remove_user_from_state(
    area_id: int, area_state: AreaState, user: "User"
) -> Tuple[AreaState, PointData]:
    try:
        from_point_data = _get_user_state_point_position_by_user_id(
            user_id=user.id, area_state=area_state
        )
        area_state[from_point_data.x][from_point_data.y] = AreaItem.zero(
            area_id=area_id
        )
    except UserNotFoundInStateException:
        pass

    return area_state, from_point_data


def _add_user_to_state(
    area_id: int, area_state: AreaState, user: "User", point: PointData, **kwargs
) -> AreaState:
    room = kwargs.pop("room", None)
    area_state[point.x][point.y] = AreaItem.from_user(
        user=user, area_id=area_id, x=point.x, y=point.y, room=room
    )

    return area_state


def get_area_items_for_connected_users_by_id(area_id: int) -> List[Dict[str, Any]]:
    area_state, _, _ = _get_or_create_area_state_by_area_id(area_id=area_id)
    connected_ids = _get_connected_ids_in_area_state_by_state(area_state=area_state)

    return [x.to_dict() for x in connected_ids]


def remove_user_from_area_by_area_and_user_id(
    area_id: int, user_id: int
) -> List[Dict[str, Any]]:
    area_state, area, _ = _get_or_create_area_state_by_area_id(area_id=area_id)
    user_point_data = _get_user_state_point_position_by_user_id(
        user_id=user_id, area_state=area_state
    )

    area_state[user_point_data.x][user_point_data.y] = AreaItem.zero(area_id=area_id)

    area = _serialize_and_commit_area_state(area=area, area_state=area_state)

    return [
        area_item
        for area_item in _get_connected_ids_in_area_state_by_state(
            area_state=area_state
        )
    ]


def move_user_to_point_in_area_state_by_area_user_and_room(
    area_id: int, user: "User", to_point_data: PointData, room: str
) -> MovementData:
    """
    Allow to move the user in area and return a MovementData info
    The user move could be an initial movement.
    """
    area_state, area, _ = _get_or_create_area_state_by_area_id(area_id=area_id)

    # Remove user from area
    area_state, from_point_data = _remove_user_from_state(
        area_id=area_id, area_state=area_state, user=user
    )

    # Add user to area

    area_state = _add_user_to_state(
        area_id=area_id,
        area_state=area_state,
        user=user,
        point=to_point_data,
        room=room,
    )

    _serialize_and_commit_area_state(area=area, area_state=area_state)

    return MovementData(
        from_point=from_point_data, to_point=to_point_data, user_id=user
    )
