from rest_framework.viewsets import ModelViewSet

from apps.core import models as core_models
from apps.core.api import serializers


class CompanyViewSet(ModelViewSet):
    serializer_class = serializers.CompanySerializer

    def get_queryset(self, *args, **kwargs):
        return core_models.Company.objects.all()


class AreaViewSet(ModelViewSet):
    serializer_class = serializers.AreaSerializer

    def get_queryset(self, *args, **kwargs):
        # TODO: Filter by user
        return core_models.Area.objects.filter(company__pk=1)
