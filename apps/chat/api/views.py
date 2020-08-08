import logging
import uuid

from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.utils import openfire
from apps.chat import models as chat_models
from apps.users import models as users_models
from django.conf import settings
from rest_framework import exceptions, views, generics
from rest_framework.response import Response
from twilio.rest import Client

logger = logging.getLogger(__name__)


class GetOrCreateRoomAPIView(views.APIView):
    serializer_class = serializers.GetOrCreateRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data["many"]:
            room = self.get_one_to_one_room(serializer.validated_data)
        else:
            raise exceptions.ValidationError({"many"})

        return Response({"id": room.id}, status=200)

    def get_one_to_one_room(self, validated_data: dict) -> chat_models.Room:
        try:
            return (
                chat_uc.RoomCreate(
                    self.request.user.company, validated_data["members"],
                )
                .execute()
                .get_room()
            )
        except chat_uc.NonExistentMemberException:
            raise exceptions.ValidationError('Member not exist')


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
    queryset = users_models.User.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().filter(company=self.request.user.company)

        ids = (
            chat_models.Message.objects.order_by("user__id")
            .distinct("user__id")
            .values_list("user__id", flat=True)
        )

        ids = [x for x in ids if id != self.request.user.id]

        return qs.filter(id__in=ids)[:3]
