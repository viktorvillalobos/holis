from typing import Dict, List

from django.conf import settings

from apps.core.uc.area_uc import ClearStateAreaUC, GetStateAreaUC, SaveStateAreaUC

from .lib.dataclasses import AreaData, Point
from .providers import area as area_providers


def get_area(area_id: int) -> AreaData:
    area = area_providers.get_area_instance(area_id)
    return AreaData.load_from_model(area)


def get_area_state(area_id: int) -> List[Dict]:
    area = area_providers.get_area_instance(area_id)
    return GetStateAreaUC(area).execute()


def add_user_to_area(
    area_id: int, user: settings.AUTH_USER_MODEL, point: Point, room: str
) -> Point:
    area = area_providers.get_area_instance(area_id)
    return SaveStateAreaUC(area).execute(user, point.x, point.y, room)


def remove_user_from_area(area_id: int, user: settings.AUTH_USER_MODEL) -> bool:
    area = area_providers.get_area_instance(area_id)
    try:
        ClearStateAreaUC(area).execute(user)
        return True
    except Exception:
        return False
