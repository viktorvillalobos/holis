import logging

from django.conf import settings
from rest_framework import exceptions, generics, views
from rest_framework.response import Response
from twilio.rest import Client

from apps.chat import models as chat_models
from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.users import models as users_models

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
            return (
                chat_uc.RoomCreate(
                    self.request.user.company,
                    [self.request.user.id, validated_data["to"]],
                )
                .execute()
                .get_room()
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


class RecentChatsAPIView(generics.ListAPIView):
    serializer_class = serializers.RecentsSerializer
    queryset = chat_models.Message.objects.all()
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset().filter(company=self.request.user.company)

        last_room_ids = (
            qs.filter(room__is_one_to_one=True)
            .order_by("room__id")
            .distinct("room__id")
            .values_list("room_id", flat=True)
        )[:3]

        users_ids = (
            chat_models.Room.objects.filter(id__in=last_room_ids)
            .order_by("members__id")
            .distinct("members__id")
            .values_list("members__id", flat=True)
        )

        users_ids = [x for x in users_ids if x != self.request.user.id]

        return users_models.User.objects.filter(id__in=users_ids)


class MessageListAPIView(generics.ListAPIView):
    queryset = chat_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            room__id=self.kwargs["id"], company=self.request.user.company
        ).order_by("-created")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(reversed(page), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
