from apps.core import models as core_models
from apps.core.api import serializers
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from apps.core.views.mixins import CompanyMixinViewSet


class CompanyViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = core_models.Company.objects.all()


class AreaViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.AreaSerializer
    queryset = core_models.Area.objects.all()


class AnnouncementViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.AnnouncementSerializer
    queryset = core_models.Announcement.objects.all()

    def get_queryset(self):
        return self.queryset.filter(company=self.request.company)


class ChangeLogViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.ChangeLogSerializer
    queryset = core_models.ChangeLog.objects.all()
