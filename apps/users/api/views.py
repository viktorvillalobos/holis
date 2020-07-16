import uuid

from apps.core import models as core_models
from apps.users import models
from apps.users.api import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
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
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filterset_fields = ("name", "email", "username")

    def get_queryset(self, *args, **kwargs):
        return self.queryset.exclude(id=self.request.user.id)

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
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        name = self.kwargs.get('company_name')
        return get_object_or_404(core_models.Company, code__iexact=name)


class SetStatusAPIView(views.APIView):
    serializer_class = serializers.SetStatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        status_id = serializer.validated_data["status_id"]
        models.Status.objects.filter(user=self.request.user).update(is_active=False)
        status = models.Status.objects.get(id=status_id)
        status.is_active = True
        status.save()
        return Response(status=200)
