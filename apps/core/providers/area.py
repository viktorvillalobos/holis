from typing import Any, Dict, List

from apps.core.models import Area


def get_area_instance_by_id(area_id: int) -> Area:
    return Area.objects.get(id=area_id)
