from typing import Dict, Iterable, Union

from django.db.models import Count
from django.db.models.query import QuerySet

import uuid
from uuid import UUID

from ..models import Room


def get_or_create_one_to_one_room_by_members_ids(
    company_id: int, to_user_id: int, from_user_id: int
) -> Room:
    try:
        return (
            Room.objects.filter(
                company_id=company_id,
                members__id__in={from_user_id, to_user_id},
                is_one_to_one=True,
            )
            .annotate(num_members=Count("members"))
            .filter(num_members=2)
            .earliest("created")
        )
    except Room.DoesNotExist:
        return Room.objects.create(
            **{
                "company_id": company_id,
                "is_one_to_one": True,
                "name": str(uuid.uuid4()),
                "any_can_invite": False,
                "members_only": True,
                "max_users": 2,
            }
        )


def create_many_to_many_room_by_name(
    company_id: int, name: str, any_can_invite: bool = True
) -> Room:
    return Room.objects.create(
        **{
            "company_id": company_id,
            "is_one_to_one": False,
            "name": name,
            "any_can_invite": any_can_invite,
            "members_only": True,
            "max_users": -1,
        }
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
