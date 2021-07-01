from typing import Any, Dict, List, Optional

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

import logging

from apps.core import models as core_models
from apps.core.cachekeys import USER_POSITION_KEY
from apps.users import models as users_models

logger = logging.getLogger(__name__)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Status
        fields = ["text", "icon", "icon_text", "is_active", "id"]


class CompanyField(serializers.Field):
    def to_representation(self, company):
        return {
            "name": company.name,
            "logo": company.logo.url,
            "logo_thumb": company.logo_thumb,
        }

    def to_internal(self, data):
        return data


class UserCompanySerializer(serializers.ModelSerializer):
    logo_thumb = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = core_models.Company
        fields = ["id", "name", "logo", "logo_thumb"]

    def get_logo_thumb(self, obj):
        if not obj.logo_thumb:
            return None

        # TODO: This serializer is used in channel consumer
        # this object not have the request object
        # we need to create a converter from scope to request
        # to use drf serlaizers
        try:
            return self.context["request"].build_absolute_uri(obj.logo_thumb)
        except KeyError:
            return obj.logo_thumb


def serialize_user_queryset(queryset: QuerySet) -> List[Dict[str, Any]]:
    results = [
        {
            "id": x.id,
            "birthday": x.birthday,
            "email": x.email,
            "name": x.name,
            "position": x.position,
            "statuses": [
                {
                    "text": status.text,
                    "icon": status.icon.url if status.icon else None,
                    "icon_text": status.icon_text,
                    "is_active": status.is_active,
                    "id": status.id,
                }
                for status in x.statuses.all()
            ],
            "username": x.username,
            "avatar_thumb": x.avatar_thumb,
            "is_staff": x.is_staff,
        }
        for x in queryset
    ]

    return {"results": results}


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    birthday = serializers.DateField(required=False)
    company = UserCompanySerializer(read_only=True)
    email = serializers.EmailField(allow_blank=False, allow_null=False)
    name = serializers.CharField()
    room = serializers.SerializerMethodField(read_only=True)
    position = serializers.CharField()
    statuses = StatusSerializer(many=True, read_only=True)
    username = serializers.CharField()
    avatar = serializers.SerializerMethodField(read_only=True)
    avatar_thumb = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

    def get_status(self, user: "User") -> Optional[dict[str, Any]]:
        statuses = list(user.statuses.all())

        if not statuses:
            return None

        try:
            active_status = [status for status in statuses if status.is_active][0]
        except IndexError:
            return None

        return {
            "id": active_status.id,
            "text": active_status.text,
            "icon_text": active_status.icon_text,
        }

    def get_avatar(self, obj):
        try:
            return self.context["request"].build_absolute_uri(obj.avatar_thumb)
        except KeyError:
            return obj.avatar_thumb

    def get_avatar_thumb(self, obj):
        if not obj.avatar_thumb:
            return None

        # TODO: This serializer is used in channel consumer
        # this object not have the request object
        # we need to create a converter from scope to request
        # to use drf serlaizers
        try:
            return self.context["request"].build_absolute_uri(obj.avatar_thumb)
        except KeyError:
            return obj.avatar_thumb

    def get_room(self, obj):
        data = cache.get(USER_POSITION_KEY.format(obj.id)) or {}
        return data.get("room")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Notification
        fields = "__all__"


class AuthEmailTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    company = serializers.IntegerField(label=_("Company"), write_only=True)
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        company_id = attrs.get("company")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                company_id=company_id,
                email=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include 'email' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CheckCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Company
        fields = ("id", "name", "code")


class SetStatusSerializer(serializers.Serializer):
    status_id = serializers.IntegerField()


class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.User
        fields = ("avatar", "id")
