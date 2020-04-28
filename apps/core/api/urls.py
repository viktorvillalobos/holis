from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.core.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("companies", views.CompanyViewSet, basename="companies")
router.register("areas", views.AreaViewSet, basename="areas")

urlpatterns = []

urlpatterns += router.urls
