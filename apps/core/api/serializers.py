import logging
from apps.core import models as core_models
from apps.core.uc.area_uc import GetStateAreaUC
from rest_framework import serializers

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
        return GetStateAreaUC(obj).execute()

    class Meta:
        model = core_models.Area
        fields = "__all__"


class UserField(serializers.Field):
    def to_representation(self, user):
        return {
            "name": user.name,
            "position": user.position,
            "avatar": user.avatar.url,
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
