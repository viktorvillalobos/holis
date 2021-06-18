from typing import Dict, Iterable, List, Union

from django.db.models import Count
from django.db.models.query import QuerySet

from uuid import UUID

from apps.utils.cache import cache

from ..models import Room


def get_one_to_one_room_by_members_ids(company_id: int, members_ids: List[int]) -> Room:
    return (
        Room.objects.filter(
            company_id=company_id, members__id__in=members_ids, is_one_to_one=True
        )
        .annotate(num_members=Count("members"))
        .filter(num_members=2)
        .earliest("created")
    )


def get_rooms_by_uuids(
    *, company_id: int, room_uuids: Iterable[Union[UUID, str]]
) -> QuerySet:
    return Room.objects.filter(company_id=company_id, uuid__in=room_uuids).order_by(
        "uuid", "-created"
    )


def get_rooms_by_uuids_in_bulk(
    *, company_id: int, room_uuids: Iterable[Union[UUID, str]]
) -> Dict[UUID, Room]:
    return get_rooms_by_uuids(company_id=company_id, room_uuids=room_uuids).in_bulk()
