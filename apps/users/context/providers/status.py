from typing import Any, Optional

from django.core.cache import cache
from django.db.models import QuerySet

from ...lib.constants import USER_STATUS_KEY
from ..models import Status


def _set_status_cache(company_id: int, user_id: int, status: Status) -> None:
    cache.set(
        USER_STATUS_KEY.format(status.company_id, user_id),
        {"id": status.id, "icon_text": status.icon_text, "text": status.text},
        30,
    )


def get_user_statuses_by_user_id(company_id: int, user_id: int) -> QuerySet:
    return Status.objects.filter(company_id=company_id, user_id=user_id)


def inactivate_all_user_status_by_user_id(company_id: int, user_id: int) -> None:
    statuses = get_user_statuses_by_user_id(company_id=company_id, user_id=user_id)
    statuses.update(is_active=False)


def set_active_status_by_user_and_status_id(
    company_id: int, user_id: int, status_id: int
) -> None:
    new_active_status = Status.objects.get(
        company_id=company_id, user_id=user_id, id=status_id
    )

    new_active_status.is_active = True
    new_active_status.save()

    _set_status_cache(company_id=company_id, user_id=user_id, status=new_active_status)


def get_user_active_status_from_cache_by_user_id(
    company_id: int, user_id: int
) -> Optional[dict[str, Any]]:
    return cache.get(USER_STATUS_KEY.format(company_id, user_id))


def get_user_active_status_from_db_by_user_id(
    company_id: int, user_id: int
) -> Optional[Status]:
    status = Status.objects.filter(
        is_active=True, user_id=user_id, company_id=company_id
    ).first()

    if not status:
        return None

    _set_status_cache(company_id=company_id, user_id=user_id, status=status)

    return status
