from typing import Union

from django.db.models import Exists
from django.db.models.query import QuerySet
from django.utils import timezone

from uuid import UUID

from apps.chat.models import Message


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


def set_message_readed_by(
    company_id: int, message_uuid: Union[UUID, str], user_id: int
) -> Message:
    message = Message.objects.get(company_id=company_id, uuid=message_uuid)
    message.reads[user_id] = {"timestamp": timezone.now().isoformat()}
    message.save()

    return message
