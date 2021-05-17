from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.core import models as core_models
from apps.core import services as core_services
from apps.core.api import serializers
from apps.utils.mixins.views import CompanyMixinViewSet


class CompanyViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = core_models.Company.objects.all()


class AreaViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        return Response(
            core_services.get_users_connecteds_by_area_from_cache(
                company_id=self.request.user.company_id
            ),
            status=200,
        )


class AnnouncementViewSet(CompanyMixinViewSet, ModelViewSet):
    serializer_class = serializers.AnnouncementSerializer
    queryset = core_models.Announcement.objects.all()

    def get_queryset(self):
        return self.queryset.filter(company=self.request.company)


class ChangeLogViewSet(ModelViewSet):
    serializer_class = serializers.ChangeLogSerializer
    queryset = core_models.ChangeLog.objects.all()
