from django.utils import timezone

from ..models import User


def touch_user_by_user_and_area_id(user_id: int, area_id: int, ts=None) -> None:
    ts = ts or timezone.now()
    User.objects.filter(id=user_id).update(current_area_id=area_id, last_seen=ts)


def disconnect_user_by_id(user_id: int) -> None:
    User.objects.filter(id=user_id).update(current_area=None, last_seen=None)
