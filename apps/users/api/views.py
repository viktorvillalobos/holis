import uuid
import logging
import random
import os
from apps.core import models as core_models
from apps.users import models
from apps.users.api import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.validators import FileExtensionValidator
from rest_framework import generics, permissions, status, views, exceptions
from rest_framework.parsers import FileUploadParser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.web import models as web_models

User = get_user_model()

logger = logging.getLogger(__name__)


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet,
):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    filterset_fields = ("name", "email", "username")

    def get_queryset(self, *args, **kwargs):
        if self.kwargs.get("id"):
            return self.queryset.filter(company=self.request.user.company)

        return self.queryset.filter(company=self.request.user.company).exclude(
            id=self.request.user.id
        )

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = self.serializer_class(
            request.user, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["PATCH"])
    def edit(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
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


class LoginAPIView(ObtainAuthToken):
    serializer_class = serializers.AuthEmailTokenSerializer


class CheckCompanyAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.CheckCompanySerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        name = self.kwargs.get('company_name')
        return get_object_or_404(core_models.Company, code__iexact=name)


class SuggestCompanyCodeAPIView(views.APIView):
    serializer_class = serializers.CheckCompanySerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        company_name = request.GET.get('company_name')

        if not company_name:
            raise exceptions.ValidationError({"company_name": "is required"})

        code = company_name.lower().replace(" ", "-")

        if self.exists_code(code):
            return Response(
                {"recommendations": self.get_recomendations(code)}, status=406
            )
        return Response({}, status=200)

    def exists_code(self, code):
        temp_company = core_models.Company.objects.filter(
            code__iexact=code
        ).first()
        temp_lead = web_models.Lead.objects.filter(
            company_code__iexact=code
        ).first()

        return temp_company or temp_lead

    def get_recomendations(self, code):
        recs = [f'{code}{random.randint(1, 200)}' for x in range(10)]

        temp_company = core_models.Company.objects.filter(
            code__in=recs
        ).values_list("code", flat=True)

        temp_lead = web_models.Lead.objects.filter(
            company_code__in=recs
        ).values_list("company_code", flat=True)

        return [
            x for x in recs if x not in temp_company and x not in temp_lead
        ]


class SetStatusAPIView(views.APIView):
    serializer_class = serializers.SetStatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        status_id = serializer.validated_data["status_id"]
        models.Status.objects.filter(user=self.request.user).update(
            is_active=False
        )
        status = models.Status.objects.get(id=status_id)
        status.is_active = True
        status.save()
        return Response(status=200)


class UploadAvatarAPIView(views.APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, pk=self.kwargs["pk"])

        avatar = request.data.get("avatar")

        self.validate_extensions(avatar)
        user.avatar = avatar
        user.save()

        return Response(serializers.UserSerializer(user).data, status=200)

    def validate_extensions(self, avatar):
        if isinstance(avatar, str):
            return True

        valid_extensions = [".jpeg", ".jpg", ".png"]
        ext = os.path.splitext(avatar.name)[1]
        if not ext.lower() in valid_extensions:
            raise exceptions.ValidationError(
                {"avatar": "Only jpeg, jpg or png are supported"}
            )
