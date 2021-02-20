from rest_framework import serializers

import logging

from apps.core import models as core_models

from .. import services as core_services

logger = logging.getLogger(__name__)


class CustomCurrentCompany(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        _id: int = serializer_field.context["request"].user.company_id
        return core_models.Company.objects.get(id=_id)


class CustomCurrentUser(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.id


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Company
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    company = serializers.HiddenField(default=CustomCurrentCompany())
    state = serializers.SerializerMethodField()

    def get_state(self, obj):
        return core_services.get_area_state(area_id=obj.id)

    class Meta:
        model = core_models.Area
        fields = "__all__"
        read_only_fields = ("pk", "created", "updated", "state")


class UserField(serializers.Field):
    def to_representation(self, user):
        return {
            "name": user.name,
            "position": user.position,
            "avatar": user.avatar.url if user.avatar else None,
            "avatar_thumb": user.avatar_thumb,
        }


class AnnouncementSerializer(serializers.ModelSerializer):
    company = serializers.HiddenField(default=CustomCurrentCompany())
    created_by = UserField(default=serializers.CurrentUserDefault())

    class Meta:
        model = core_models.Announcement
        fields = "__all__"


class ChangeLogSerializer(serializers.ModelSerializer):
    created_by = UserField(default=serializers.CurrentUserDefault())

    class Meta:
        model = core_models.ChangeLog
        fields = "__all__"
