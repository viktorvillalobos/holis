from typing import Any, Dict, List

from apps.core.models import Area
from apps.core.uc.area_uc import GetStateAreaUC


def get_area_state_by_area(area: Area) -> List[Dict[str, Any]]:
    return GetStateAreaUC(area).execute()


def get_area_instance_by_id(area_id: int) -> Area:
    return Area.objects.get(id=area_id)
