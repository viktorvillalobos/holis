import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics, views, exceptions

from apps.utils import openfire
from apps.core import models as core_models
from apps.users import models
from apps.users.api import serializers

User = get_user_model()


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filterset_fields = ("name", "email", "username")

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = self.serializer_class(
            request.user, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def birthdays(self, request):
        users = User.objects.get_upcoming_birthdays()
        serializer = self.serializer_class(
            users, many=True, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        pass


class NotificationViewSet(ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)


class LoginAPIView(ObtainAuthToken):
    serializer_class = serializers.AuthEmailTokenSerializer


class CheckCompanyAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.CheckCompanySerializer

    def get_object(self):
        name = self.kwargs.get('company_name')
        return get_object_or_404(core_models.Company, name__iexact=name)


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
        try:
            users.update_user(jid, password=generated_code)
        except openfire.exceptions.UserNotFoundException:
            raise exceptions.ValidationError(
                "Error changing password: user not found in xmpp server"
            )
        return Response(
            {"token": generated_code, "jid": jid}, status=200
        )
