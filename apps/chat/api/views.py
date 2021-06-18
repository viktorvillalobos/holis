from django.conf import settings
from rest_framework import exceptions, generics, status, views
from rest_framework.pagination import CursorPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

import logging
from twilio.rest import Client

from apps.chat import models as chat_models
from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.chat.providers import message as message_providers
from apps.chat.providers import message_attachment as message_attachment_providers

from .. import services as chat_services
from .. import tasks as chat_tasks

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
        limit = int(request.GET.get("limit", "3"))

        return Response(
            chat_services.get_recents_rooms_by_user_id(
                company_id=self.request.company_id,
                user_id=self.request.user.id,
                is_one_to_one=True,
                limit=limit,
            ),
            status=status.HTTP_200_OK,
        )


class MessageCursoredPagination(CursorPagination):
    page_size = 10


class MessageListAPIView(generics.ListAPIView):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.MessageWithAttachmentsSerializer
    pagination_class = MessageCursoredPagination

    def get_queryset(self):
        return message_providers.get_messages_by_room_uuid(
            company_id=self.request.user.company_id,
            room_uuid=self.kwargs["room_uuid"],
            user_id=self.request.user.id,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        self.launch_set_mensages_readed_task()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(reversed(page), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def launch_set_mensages_readed_task(self):
        chat_tasks.set_messages_readed_by_room_and_user_task.delay(
            company_id=self.request.company_id,
            room_uuid=self.kwargs["room_uuid"],
            user_id=self.request.user.id,
        )
