import logging
import uuid

from apps.chat import models as chat_models
from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.utils import openfire
from django.conf import settings
from rest_framework import exceptions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from twilio.rest import Client

logger = logging.getLogger(__name__)


class ChannelViewSet(ModelViewSet):
    serializer_class = serializers.ChannelSerializer
    queryset = chat_models.Channel.objects.all()

    def get_queryset(self):
        return self.queryset.filter(company__id=self.request.user.company_id)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk):
        channel = self.get_object()
        serializer = serializers.MessageSerializer(
            channel.messages.all(), many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class GetChatCredentialsAPIView(views.APIView):
    """
        This endpoint, emulate the generation
        of custom password for xmpp, the password
        must be changed every time the user login.

        Steps:

        1) Generate custom password.
        2) Change the password using openfire api.
        3) Send the password to client.

    """

    def get_jid(self):
        self.jid = self.request.user.jid
        try:
            self.username, self.domain = self.jid.split('@')
        except Exception:
            raise exceptions.ValidationError('Bad formed JID')

    def generate_new_password(self):
        users = openfire.users.Users()
        self.generated_code = str(uuid.uuid4())
        try:
            users.update_user(self.username, password=self.generated_code)
        except openfire.exceptions.UserNotFoundException:
            raise exceptions.ValidationError(
                "Error changing password: user not found in xmpp server"
            )

    def get(self, request, *args, **kwargs):
        self.get_jid()
        self.generate_new_password()

        return Response(
            {
                "token": self.generated_code,
                "jid": self.jid,
                "domain": self.domain,
                "username": self.username,
            },
            status=200,
        )


class GetOrCreateChannelAPIView(views.APIView):
    serializer_class = serializers.GetOrCreateChannelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            channel = (
                chat_uc.CreateOneToOneChannelUC(
                    self.request.user.company,
                    serializer.validated_data["members"],
                )
                .execute()
                .get_channel()
            )
        except chat_uc.NonExistentMemberException:
            raise exceptions.ValidationError('Member not exist')
        return Response({"jid": channel.id}, status=200)


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
    pass
