import logging
from apps.core import models as core_models
from apps.core.uc.area_uc import GetStateAreaUC
from rest_framework import serializers

logger = logging.getLogger(__name__)


class CustomCurrentCompany(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        _id: int = serializer_field.context["request"].user.company_id
        return core_models.Company.objects.get(id=_id)


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


class AnnouncementSerializer(serializers.ModelSerializer):
    company = serializers.HiddenField(default=CustomCurrentCompany())

    class Meta:
        model = core_models.Announcement
        fields = "__all__"
