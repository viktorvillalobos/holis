from apps.users import models
from apps.users.api import serializers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

User = get_user_model()


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
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


class NotificationViewSet(ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)
