from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response

from apps.core import models as core_models
from apps.core.api import serializers
from apps.utils.mixins.views import CompanyMixinViewSet


class CompanyViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = core_models.Company.objects.all()


class AreaViewSet(CompanyMixinViewSet, GenericViewSet):
    serializer_class = serializers.AreaSerializer
    queryset = core_models.Area.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data

        return Response(serialized_data, status=200)


class AnnouncementViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.AnnouncementSerializer
    queryset = core_models.Announcement.objects.all()

    def get_queryset(self):
        return self.queryset.filter(company=self.request.company)


class ChangeLogViewSet(ModelViewSet):
    serializer_class = serializers.ChangeLogSerializer
    queryset = core_models.ChangeLog.objects.all()
