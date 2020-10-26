from typing import Dict, List

from apps.core.uc.area_uc import GetStateAreaUC

from .entities import Area


def get_area_state(area: Area) -> List[Dict]:
    return GetStateAreaUC(area).execute()
