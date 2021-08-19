from django.http.request import HttpRequest
from rest_framework import exceptions, generics, status, views, viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

import logging
import os
from uuid import UUID

from apps.chat.lib.exceptions import NonExistentMemberException
from apps.utils.rest_framework import objects
from apps.utils.rest_framework.paginators import CursoredAPIPagination

from ... import services as chat_services
from ... import tasks as chat_tasks
from ...context import models as chat_models
from ...context.providers import message as message_providers
from ...context.providers import message_attachment as message_attachment_providers
from . import serializers
from .pagination import MessageCursoredPagination

logger = logging.getLogger(__name__)


class GetOrCreateConversationRoomAPIView(views.APIView):
    serializer_class = serializers.GetOrCreateRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        to = serializer.validated_data["to"]

        is_a_one_to_one_room = len(to) == 1

        if is_a_one_to_one_room:
            room = self.get_one_to_one_room(to=to[0])
        else:
            room = self.get_many_to_many_room(to=to)

        return Response({"id": room.uuid}, status=200)

    def get_one_to_one_room(self, to: int) -> chat_models.Room:
        try:
            return chat_services.get_or_create_one_to_one_conversation_room_by_members_ids(
                company_id=self.request.company_id,
                from_user_id=self.request.user.id,
                to_user_id=to,
            )
        except NonExistentMemberException:
            raise exceptions.ValidationError("Member does not exist")

    def get_many_to_many_room(self, to: list[int]) -> chat_models.Room:
        try:
            return chat_services.get_or_create_many_to_many_conversation_room_by_members_ids(
                company_id=self.request.user.company_id,
                members_ids={self.request.user.id, *to},
            )
        except NonExistentMemberException:
            raise exceptions.ValidationError("Member does not exist")


class CustomRoomViewSet(viewsets.ViewSet):
    serializer_class = serializers.CreateCustomRoomSerializer

    def create(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = chat_services.create_custom_room_by_name(
            company_id=self.request.company_id, **serializer.validated_data
        )

        serialized_data = self.serializer_class(room).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


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
        # TODO: add validation

        text = request.POST.get("text")
        app_uuid = request.POST.get("app_uuid")
        files = request.FILES.getlist("files")

        message = chat_services.create_message(
            company_id=request.user.company_id,
            room_uuid=room_uuid,
            user_id=request.user.id,
            text=text,
            app_uuid=app_uuid,
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
            user=self.request.user,
        )

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class RecentRoomsAPIView(objects.ListAPIView):
    serializer_class = serializers.RecentRoomSerializer
    queryset = chat_models.Message.objects.all()
    objects_generator = staticmethod(
        chat_services.get_cursored_recents_rooms_by_user_id
    )
    pagination_class = CursoredAPIPagination

    def get_objects_generator_context(self):
        context = super().get_objects_generator_context() or {}
        context["reverse"] = True
        context["page_size"] = self.request.GET.get("page_size")
        context["company_id"] = self.request.company_id
        context["user_id"] = self.request.user.id
        context["search"] = self.request.GET.get("search")

        return context


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

        self.set_room_user_read()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(reversed(page), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def set_room_user_read(self):
        chat_tasks.set_room_user_read_task.delay(
            company_id=self.request.company_id,
            user_id=self.request.user.id,
            room_uuid=self.kwargs["room_uuid"],
        )


class RoomViewSet(viewsets.ViewSet):
    serializers_class = serializers.RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        room = chat_services.get_room_with_members_by_uuid(
            company_id=request.company_id, room_uuid=self.kwargs["room_uuid"]
        )

        serializer = self.serializers_class(room)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExitRoomViewSet(views.APIView):
    """
    Allow to the user to exist from a room
    """

    def delete(self, request: HttpRequest, **kwargs) -> Response:
        chat_services.remove_user_from_room_by_uuid(
            company_id=request.company_id,
            user_id=request.user.id,
            room_uuid=kwargs["room_uuid"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadRoomImageViewSet(viewsets.ViewSet):
    parser_class = (FileUploadParser,)

    def partial_update(self, request, *args, **kwargs):
        image = request.data.get("image")

        self.validate_extensions(image)

        room = chat_services.update_room_image_by_uuid(
            company_id=request.company_id,
            room_uuid=self.kwargs["room_uuid"],
            image=image,
        )

        return Response(
            serializers.RoomSerializer(room).data, status=status.HTTP_200_OK
        )

    def validate_extensions(self, avatar):
        if isinstance(avatar, str):
            return True

        valid_extensions = [".jpeg", ".jpg", ".png"]
        ext = os.path.splitext(avatar.name)[1]
        if not ext.lower() in valid_extensions:
            raise exceptions.ValidationError(
                {"avatar": "Only jpeg, jpg or png are supported"}
            )
