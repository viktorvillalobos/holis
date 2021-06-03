from typing import Union

from django.db.models.query import QuerySet

from uuid import UUID

from apps.chat.models import Message


def get_messages_by_room_uuid(company_id: int, room_uuid: Union[str, UUID]) -> QuerySet:
    return (
        Message.objects.filter(company_id=company_id, room__uuid=room_uuid)
        .select_related("user", "room")
        .prefetch_related("attachments")
        .order_by("-created")
    )
