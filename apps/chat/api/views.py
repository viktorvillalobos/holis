import logging
import uuid

from apps.chat import uc as chat_uc
from apps.chat.api import serializers
from apps.utils import openfire
from apps.chat.models import openfire as of_models
from apps.users import models as users_models
from django.conf import settings
from rest_framework import exceptions, views
from rest_framework.response import Response
from twilio.rest import Client

logger = logging.getLogger(__name__)


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


# class GetOrCreateChannelAPIView(views.APIView):
#     serializer_class = serializers.GetOrCreateChannelSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             channel = (
#                 chat_uc.CreateOneToOneChannelUC(
#                     self.request.user.company,
#                     serializer.validated_data["members"],
#                 )
#                 .execute()
#                 .get_channel()
#             )
#         except chat_uc.NonExistentMemberException:
#             raise exceptions.ValidationError('Member not exist')
#         return Response({"jid": channel.id}, status=200)


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
    def get(self, request, *args, **kwargs):
        ids = list(
            set(
                of_models.OfMessageArchive.objects.using("openfire")
                .order_by("-messageid")
                .values_list("fromjid", flat=True)
            )
        )

        users = users_models.User.objects.filter(jid__in=ids)[:3]
        results = [{"jid": x.jid, "name": x.name, "avatar_thumb": x.avatar_thumb} for x in users]
        return Response(results, status=200)
