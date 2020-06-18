import uuid
import logging
from apps.chat import models
from apps.chat.api import serializers
from rest_framework import status, exceptions, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from apps.utils import openfire
from apps.chat import models as chat_models
from apps.chat import uc as chat_uc

logger = logging.getLogger(__name__)


class ChannelViewSet(ModelViewSet):
    serializer_class = serializers.ChannelSerializer
    queryset = models.Channel.objects.all()

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

    def get(self, request, *args, **kwargs):
        generated_code = str(uuid.uuid4())
        users = openfire.users.Users()
        jid = self.request.user.jid
        if not jid:
            raise exceptions.ValidationError(
                {"jid": "User does not have JID assigned"}
            )

        try:
            users.update_user(jid, password=generated_code)
        except openfire.exceptions.UserNotFoundException:
            raise exceptions.ValidationError(
                "Error changing password: user not found in xmpp server"
            )
        return Response({"token": generated_code, "jid": jid}, status=200)


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
