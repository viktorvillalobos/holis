from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.core import models as core_models
from apps.core.api import serializers


class CompanyViewSet(ModelViewSet):
    serializer_class = serializers.CompanySerializer

    def get_queryset(self, *args, **kwargs):
        return core_models.Company.objects.all()


class AreaViewSet(ModelViewSet):
    serializer_class = serializers.AreaSerializer
    queryset = core_models.Area.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(company__pk=self.request.user.company_id)


class AnnouncementViewSet(ModelViewSet):
    serializer_class = serializers.AnnouncementSerializer
    queryset = core_models.Announcement.objects.all()
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return self.queryset.filter(company__pk=self.request.user.company_id)
