from typing import Any, Optional

from django.core.cache import cache
from django.db.models import QuerySet

from ..lib.constants import USER_STATUS_KEY
from ..models import Status


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

    cache.set(
        USER_STATUS_KEY.format(company_id, user_id),
        {
            "id": new_active_status.id,
            "icon_text": new_active_status.icon_text,
            "text": new_active_status.text,
        },
    )


def get_user_active_status_from_cache_by_user_id(
    company_id: int, user_id: int
) -> Optional[dict[str, Any]]:
    return cache.get(USER_STATUS_KEY.format(company_id, user_id))


def get_user_active_status_from_db_by_user_id(
    company_id: int, user_id: int
) -> Optional[Status]:
    return Status.objects.filter(
        is_active=True, user_id=user_id, company_id=company_id
    ).first()
