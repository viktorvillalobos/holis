from typing import Optional

from django.db.models import QuerySet
from django.utils import timezone

from ..models import User


def get_user_by_id(user_id: int) -> User:
    return User.objects.get(id=user_id)


def touch_user_by_user_and_area_id(user_id: int, area_id: int, ts=None) -> None:
    ts = ts or timezone.now()
    User.objects.filter(id=user_id).update(current_area_id=area_id, last_seen=ts)


def disconnect_user_by_id(user_id: int) -> None:
    User.objects.filter(id=user_id).update(current_area=None, last_seen=None)


def get_users_with_statuses(
    company_id: int,
    user_id: Optional[int] = None,
    include_myself: Optional[bool] = False,
    name: Optional[str] = None,
) -> QuerySet:
    queryset = User.objects.filter(company_id=company_id).prefetch_related("statuses")

    if not include_myself:
        queryset = queryset.exclude(id=user_id)

    if name:
        queryset = queryset.filter(name__icontains=name)

    return queryset
