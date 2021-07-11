from typing import Dict, Iterable, List, Optional, Union

from django.db.models import Case, Count, Exists, Q, Value, When
from django.db.models.expressions import OuterRef
from django.db.models.query import QuerySet

from datetime import datetime
from uuid import UUID

from apps.utils.cache import cache
from apps.utils.html import strip_tags
from apps.utils.rest_framework.paginators import get_paginated_queryset

from ..models import Message, Room, RoomUserRead


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


def get_recents_rooms_by_user_id(
    *,
    company_id: int,
    user_id: int,
    is_one_to_one: bool = True,
    search: Optional[str] = None,
    cursor: Optional[dict[str, str]] = None,
    page_size: Optional[int] = 200,
    reverse: Optional[bool] = True,
) -> tuple[list[QuerySet], Optional[dict[str, str]], Optional[dict[str, str]]]:
    message_after_last_message = Message.objects.filter(
        user_id=user_id,
        company_id=OuterRef("company_id"),
        room_uuid=OuterRef("uuid"),
        created__gte=OuterRef("last_message_ts"),
    )

    readed_after_last_message = RoomUserRead.objects.filter(
        company_id=company_id,
        user_id=user_id,
        room_uuid=OuterRef("uuid"),
        timestamp__gte=OuterRef("last_message_ts"),
    )

    room_messages = Message.objects.filter(
        company_id=OuterRef("company_id"), room_uuid=OuterRef("uuid")
    )

    have_unread_messages = Case(
        When(~Exists(room_messages), then=Value(False)),
        When(Exists(message_after_last_message), then=Value(False)),
        When(Exists(readed_after_last_message), then=Value(False)),
        default=Value(True),
    )

    queryset = (
        Room.objects.filter(
            company_id=company_id,
            members__id__in=[user_id],
            is_one_to_one=is_one_to_one,
        )
        .exclude(last_message_user_id__isnull=True)
        .prefetch_related("members")
        .annotate(have_unread_messages=have_unread_messages)
        .order_by("have_unread_messages", "-last_message_ts")
    )

    if search:
        queryset = queryset.filter(
            Q(members__name__icontains=search) | Q(name__icontains=search)
        )

    return get_paginated_queryset(
        queryset,
        cursor=cursor,
        page_size=page_size,
        reverse=reverse,
        order_column="have_unread_messages",
    )


def update_room_last_message_by_room_uuid(
    *,
    company_id: int,
    user_id: int,
    room_uuid: Union[str, UUID],
    text: str,
    ts: datetime,
) -> int:
    return Room.objects.filter(company_id=company_id, uuid=room_uuid).update(
        last_message_ts=ts,
        last_message_text=strip_tags(text),
        last_message_user_id=user_id,
    )
