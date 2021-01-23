from django.conf import settings
from rest_framework import exceptions, generics, views
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination

import logging
from twilio.rest import Client

from apps.chat import models as chat_models
from apps.chat import uc as chat_uc
from apps.chat.api import serializers

from ..services import get_recents_rooms, get_or_create_room_by_company_and_members_ids

logger = logging.getLogger(__name__)


class GetOrCreateRoomAPIView(views.APIView):
    serializer_class = serializers.GetOrCreateRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = self.get_one_to_one_room(serializer.validated_data)

        return Response({"id": room.id}, status=200)

    def get_one_to_one_room(self, validated_data: dict) -> chat_models.Room:
        try:
            return get_or_create_room_by_company_and_members_ids(
                company_id=self.request.user.company_id,
                members_ids=[self.request.user.id, validated_data["to"]],
            )
        except chat_uc.NonExistentMemberException:
            raise exceptions.ValidationError("Member not exist")


class GetTurnCredentialsAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        account_sid = settings.TWILIO_ACCOUNT_ID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        token = client.tokens.create(ttl=60)

        return Response(token.ice_servers, status=200)


class UploadFileAPIView(views.APIView):
    pass


class RecentChatsAPIView(views.APIView):
    serializer_class = serializers.RecentsSerializer
    queryset = chat_models.Message.objects.all()
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return Response(get_recents_rooms(self.request.user.id), status=200)


class MessageCursoredPagination(CursorPagination):
    page_size = 10


class MessageListAPIView(generics.ListAPIView):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.MessageRawSerializer
    pagination_class = MessageCursoredPagination

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(room__id=self.kwargs["id"], company_id=self.request.user.company_id)
            .select_related("user", "room")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(reversed(page), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
