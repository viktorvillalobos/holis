from typing import Optional

from django.conf import settings
from rest_framework import exceptions, generics, status, views
from rest_framework.pagination import CursorPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

import logging
from collections import OrderedDict
from datetime import datetime
from twilio.rest import Client

from apps.chat import models as chat_models
from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.chat.providers import message as message_providers
from apps.chat.providers import message_attachment as message_attachment_providers
from apps.chat.providers import room_read as room_read_providers
from apps.chat.providers.room_read import get_room_read_by_user_and_room_uuid

from .. import services as chat_services

logger = logging.getLogger(__name__)


class GetOrCreateRoomAPIView(views.APIView):
    serializer_class = serializers.GetOrCreateRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = self.get_one_to_one_room(serializer.validated_data)

        return Response({"id": room.uuid}, status=200)

    def get_one_to_one_room(self, validated_data: dict) -> chat_models.Room:
        try:
            return chat_services.get_or_create_room_by_company_and_members_ids(
                company_id=self.request.user.company_id,
                members_ids=[self.request.user.id, validated_data["to"]],
            )
        except chat_uc.NonExistentMemberException:
            raise exceptions.ValidationError("Member not exist")


class GetTurnCredentialsAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        credentials = chat_services.get_twilio_credentials_by_user_id(
            user_id=self.request.user.id
        )

        return Response(credentials.ice_servers, status=200)


class UploadFileAPIView(views.APIView):
    parser_classes = [MultiPartParser]
    pagination_class = None

    def post(self, request, room_uuid, *args, **kwargs):
        text = request.POST.get("text")
        files = request.FILES.getlist("files")

        message = chat_services.create_message(
            company_id=request.user.company_id,
            room_uuid=room_uuid,
            user_id=request.user.id,
            text=text,
        )

        message_attachment_providers.create_message_attachments_by_message_uuid(
            company_id=self.request.user.company_id,
            message_uuid=message.uuid,
            files=files,
        )

        serialized_data = serializers.MessageWithAttachmentsSerializer(
            message, context={"request": request}
        ).data

        chat_services.broadcast_chat_message_with_attachments(
            company_id=self.request.user.company_id,
            room_uuid=room_uuid,
            message_uuid=message.uuid,
        )

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class RecentChatsAPIView(views.APIView):
    serializer_class = serializers.RecentsSerializer
    queryset = chat_models.Message.objects.all()
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return Response(
            chat_services.get_recents_rooms(self.request.user.id), status=200
        )


class MessageCursoredPagination(CursorPagination):
    page_size = 10


class MessageListAPIView(generics.ListAPIView):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.MessageWithAttachmentsSerializer
    pagination_class = MessageCursoredPagination

    def get_queryset(self):
        return message_providers.get_messages_by_room_uuid(
            company_id=self.request.user.company_id, room_uuid=self.kwargs["room_uuid"]
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = reversed(self.paginate_queryset(queryset))
        serialized_data = self.get_serializer(page, many=True).data

        # TODO: We need to found a better way to do this

        serialized_paginated_data = self.get_paginated_response(serialized_data).data
        serialized_paginated_data[
            "last_read_timestamp"
        ] = self.get_last_read_timestamp_isoformat()

        return Response(serialized_paginated_data, status=200)

    def get_last_read_timestamp_isoformat(self) -> Optional[str]:
        try:
            return room_read_providers.get_room_read_by_user_and_room_uuid(
                company_id=self.request.user.company_id,
                user_id=self.request.user.id,
                room_uuid=self.kwargs["room_uuid"],
            ).timestamp.isoformat()
        except chat_models.RoomRead.DoesNotExist:
            return None
