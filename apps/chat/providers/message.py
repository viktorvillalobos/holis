from typing import Union

from django.db.models import Exists
from django.db.models.query import QuerySet
from django.utils import timezone

from datetime import datetime
from uuid import UUID

from apps.chat.models import Message
from apps.utils.models import InsertJSONValue


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


def get_recents_messages_by_user_id(
    *, user_id: int, is_one_to_one: bool = True, limit: int = 3
) -> QuerySet:
    return (
        Message.objects.filter(
            room__is_one_to_one=is_one_to_one, room__members__id=user_id
        )
        .order_by("room__uuid", "-created")
        .distinct("room__uuid")
    )[:limit]
