from typing import Any, Dict, List

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from datetime import timedelta

from apps.core.lib.constants import USER_POSITION_KEY
from apps.core.uc import area_uc
from apps.users import services as user_services
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .custom_types import AreaState
from .lib.dataclasses import AreaData, PointData
from .providers import area as area_providers


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


def get_users_connecteds_by_area(company_id: int, area_id: int):
    connected_users_keys = cache.keys(USER_POSITION_KEY.format(company_id, "*"))
    user_position_values = cache.get_many(connected_users_keys).items()

    one_minute_ago = timezone.now() - timedelta(seconds=60)

    to_disconnect_user_ids = []
    for key, value in user_position_values:
        if value["timestamp"] < one_minute_ago:
            _, _, _, user_id, _ = key.split("-")
            to_disconnect_user_ids.append((user_id, value["area_id"]))
