from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, generics, permissions, status, views, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

import logging
import os
import random
from dataclasses import asdict

from apps.core.context import models as core_models
from apps.web import models as web_models

from ... import services as user_services
from ... import tasks as user_tasks
from ...context import models
from ...context.providers import user as users_providers
from . import serializers
from .pagination import UserCursoredPagination

User = get_user_model()

logger = logging.getLogger(__name__)


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    pagination_class = UserCursoredPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        include_myself = bool(self.request.GET.get("include_myself", False))
        name_param = self.request.GET.get("name")

        return users_providers.get_users_with_statuses(
            company_id=self.request.company_id,
            user_id=self.request.user.id,
            include_myself=include_myself,
            name=name_param,
        )


class UserProfileViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request):
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["patch"])
    def edit(self, request):
        to_validate_data = {"company_id": self.request.company_id, **request.data}

        serializer = serializers.UserProfileUpdateSerializer(
            request.user, data=to_validate_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user_services.update_user_profile(**serializers.validated_data)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class BirthdaysViewSet(GenericViewSet, ListModelMixin):
    queryset = User.objects.get_upcoming_birthdays()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = serializers.serialize_user_queryset(queryset)
        return Response(status=status.HTTP_200_OK, data=serialized_data)


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
        name = self.kwargs.get("company_name")
        return get_object_or_404(core_models.Company, code__iexact=name)


class SuggestCompanyCodeAPIView(views.APIView):
    serializer_class = serializers.CheckCompanySerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        company_name = request.GET.get("company_name")

        if not company_name:
            raise exceptions.ValidationError({"company_name": "is required"})

        code = company_name.lower().replace(" ", "-")

        if self.exists_code(code):
            return Response(
                {"recommendations": self.get_recomendations(code)}, status=406
            )
        return Response({}, status=200)

    def exists_code(self, code):
        temp_company = (
            core_models.Company.objects.filter(code__exact=code).only("id").first()
        )
        temp_lead = (
            web_models.Lead.objects.filter(company_code__exact=code).only("id").first()
        )

        return temp_company or temp_lead

    def get_recomendations(self, code):
        recs = [f"{code}{random.randint(1, 200)}" for x in range(10)]

        temp_company = core_models.Company.objects.filter(code__in=recs).values_list(
            "code", flat=True
        )

        temp_lead = web_models.Lead.objects.filter(company_code__in=recs).values_list(
            "company_code", flat=True
        )

        return [x for x in recs if x not in temp_company and x not in temp_lead]


class SetStatusAPIView(views.APIView):
    serializer_class = serializers.SetStatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        status_id = serializer.validated_data["status_id"]
        user_services.set_user_status_by_user_and_status_id(
            company_id=request.user.company_id,
            user_id=request.user.id,
            status_id=status_id,
        )
        return Response(status=200)


class UploadAvatarAPIView(views.APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")

        self.validate_extensions(avatar)
        user = request.user
        user.avatar.save(avatar.name, avatar)

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


class UserInvitationViewSet(viewsets.ViewSet):
    serializer_class = serializers.InvitateSerializer

    def create(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        users_invitations_data = user_services.create_users_invitations(
            company_id=request.company_id,
            emails=serializer.validated_data["emails"],
            user_id=request.user.id,
        )

        invitation_values = [
            asdict(invitation) for invitation in users_invitations_data
        ]

        user_tasks.send_users_invitations.delay(invitation_values)

        return Response(status=status.HTTP_200_OK)
