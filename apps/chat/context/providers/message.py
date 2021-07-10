from typing import Union

from django.db.models import Exists
from django.db.models.query import QuerySet

from uuid import UUID

from apps.utils.models import InsertJSONValue

from ...context.models import Message


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
