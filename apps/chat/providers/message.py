from typing import Any, Optional, Union

from django.db.models import Exists, Q
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet

from uuid import UUID

from apps.chat.models import Message
from apps.utils.models import InsertJSONValue
from apps.utils.rest_framework.paginators import get_paginated_queryset


def get_messages_by_room_uuid(
    company_id: int, room_uuid: Union[UUID, str], user_id: int
) -> QuerySet:
    is_readed_queryset = Message.objects.filter(reads__has_key=str(user_id))

    return (
        Message.objects.filter(company_id=company_id, room__uuid=room_uuid)
        .select_related("user", "room")
        .prefetch_related("attachments")
        .annotate(is_readed=Exists(is_readed_queryset))
    )


def create_message(
    company_id: int, user_id: int, room_uuid: Union[UUID, str], text: str
):
    return Message.objects.create(
        company_id=company_id, room_uuid=room_uuid, user_id=user_id, text=text
    )


def set_messages_readed_by_room_and_user(
    company_id: int, room_uuid: Union[UUID, str], user_id: int
) -> int:
    return (
        Message.objects.filter(company_id=company_id, room_uuid=room_uuid)
        .exclude(reads__has_key=str(user_id))
        .update(
            reads=InsertJSONValue(
                "reads", keyname=str(user_id), new_value=True, create_missing=False
            )
        )
    )


RECENT_INFO = list[dict[str, Any]]


def get_recents_messages_values_by_user_id(
    *,
    company_id: int,
    user_id: int,
    is_one_to_one: bool = True,
    search: Optional[str] = None,
    cursor: Optional[dict[str, str]] = None,
    page_size: Optional[int] = 200,
    reverse: Optional[bool] = False,
) -> tuple[list[RECENT_INFO], Optional[dict[str, str]], Optional[dict[str, str]]]:
    is_readed_queryset = Message.objects.filter(reads__has_key=str(user_id))

    queryset = (
        Message.objects.filter(
            company_id=company_id,
            room__is_one_to_one=is_one_to_one,
            room__members__id__in=[user_id],
        )
        .annotate(have_unread_messages=Exists(is_readed_queryset))
        .values("room_uuid", "have_unread_messages", "text", "created")
        .order_by("room__uuid", "have_unread_messages", "-created")
        .distinct("room__uuid")
    )

    if search:
        queryset = queryset.filter(
            Q(room__members__name__icontains=search) | Q(room__name__icontains=search)
        )

    return get_paginated_queryset(
        queryset,
        cursor=cursor,
        page_size=page_size,
        reverse=reverse,
        order_column="room__uuid",
    )
