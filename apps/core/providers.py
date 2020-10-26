from .models import Area


def get_area_instance(area_id: int) -> Area:
    return Area.objects.get(id=area_id)
