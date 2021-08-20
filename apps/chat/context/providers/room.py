from typing import Dict, Iterable, Optional, Union

from django.core.files.base import File
from django.db import IntegrityError
from django.db.models import Case, Count, Exists, Q, Value, When
from django.db.models.expressions import OuterRef
from django.db.models.query import QuerySet

import uuid
from datetime import datetime
from uuid import UUID

from apps.users.context.models import User
from apps.utils.cache import cache
from apps.utils.html import strip_tags
from apps.utils.rest_framework.paginators import get_paginated_queryset

from ...lib.exceptions import (
    NonExistentMemberException,
    RoomDoesNotExist,
    RoomNameAlreadyExist,
)
from ..models import Message, Room, RoomUserRead


def _get_room_name_by_members_ids(members_ids: Iterable[int]) -> str:
    members_names = list(
        User.objects.filter(id__in=members_ids).values_list("name", flat=True)
    )

    members_names = sorted(members_names)
    return ", ".join(members_names)


def get_or_create_one_to_one_conversation_room_by_members_ids(
    company_id: int, to_user_id: int, from_user_id: int
) -> Room:
    try:
        return (
            Room.objects.filter(
                company_id=company_id,
                members__id__in={from_user_id, to_user_id},
                is_conversation=True,
                is_one_to_one=True,
            )
            .annotate(num_members=Count("members"))
            .filter(num_members=2)
            .earliest("created")
        )
    except Room.DoesNotExist:

        room_name = _get_room_name_by_members_ids(
            members_ids={to_user_id, from_user_id}
        )

        return Room.objects.create(
            **{
                "company_id": company_id,
                "is_one_to_one": True,
                "is_conversation": True,
                "name": room_name,
                "any_can_invite": False,
                "members_only": True,
                "max_users": 2,
            }
        )


def get_or_create_many_to_many_conversation_room_by_members_ids(
    company_id: int, members_ids: set[int]
) -> Room:
    try:
        return (
            Room.objects.filter(
                company_id=company_id,
                members__id__in=members_ids,
                is_conversation=True,
                is_one_to_one=True,
            )
            .annotate(num_members=Count("members"))
            .filter(num_members=2)
            .earliest("created")
        )
    except Room.DoesNotExist:

        room_name = _get_room_name_by_members_ids(members_ids=members_ids)

        return Room.objects.create(
            **{
                "company_id": company_id,
                "name": room_name,
                "is_conversation": True,
                "is_one_to_one": False,
                "any_can_invite": False,
                "members_only": True,
                "max_users": len(members_ids),
            }
        )


def create_custom_room_by_name(
    company_id: int,
    name: str,
    admins_ids: set[int],
    members_ids: set[int],
    is_public: bool = True,
    any_can_invite: bool = True,
) -> Room:

    try:
        room = Room.objects.create(
            name=name,
            company_id=company_id,
            is_conversation=False,
            is_one_to_one=False,
            is_public=is_public,
            any_can_invite=any_can_invite,
            is_persistent=True,
            max_users=0,
        )
    except IntegrityError as ex:
        if "unique constraint" in str(ex):
            raise RoomNameAlreadyExist

    room.admins.set(admins_ids)
    room.members.set(members_ids)

    return Room.objects.prefetch_related("members", "admins").get(uuid=room.uuid)


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
    search: Optional[str] = None,
    cursor: Optional[dict[str, str]] = None,
    page_size: Optional[int] = 200,
    reverse: Optional[bool] = True,
) -> tuple[list[Room], Optional[dict[str, str]], Optional[dict[str, str]]]:

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

    is_one_to_one_and_not_have_messages = Q(last_message_user_id__isnull=True) & Q(
        is_one_to_one=True
    )

    queryset = (
        Room.objects.filter(company_id=company_id, members__id__in=[user_id])
        .exclude(is_one_to_one_and_not_have_messages)
        .prefetch_related("members")
        .annotate(have_unread_messages=have_unread_messages)
        .order_by("have_unread_messages", "-last_message_ts", "is_conversation")
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


def get_room_with_members_by_uuid(company_id: int, room_uuid: Union[UUID, str]) -> Room:
    try:
        return Room.objects.prefetch_related("members", "admins").get(
            company_id=company_id, uuid=room_uuid
        )
    except Room.DoesNotExist:
        raise RoomDoesNotExist


def update_room_image_by_uuid(
    company_id: int, room_uuid: Union[UUID, str], image: File
) -> Room:
    room = Room.objects.get(company_id=company_id, uuid=room_uuid)
    room.image = image
    room.save()

    return room


def remove_user_from_room_by_uuid(
    company_id: int, user_id: int, room_uuid: Union[UUID, str]
) -> None:
    """
    Remove user from a room
    """

    try:
        room = Room.objects.prefetch_related("members").get(
            company_id=company_id, uuid=room_uuid
        )
    except Room.DoesNotExist:
        raise RoomDoesNotExist

    users = iter(room.members.all())

    try:
        user = next(user for user in users if user.id == user_id)
    except StopIteration:
        raise NonExistentMemberException

    room.members.remove(user)
