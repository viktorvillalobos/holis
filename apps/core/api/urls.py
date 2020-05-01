from apps.core.api import views
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("companies", views.CompanyViewSet, basename="companies")
router.register("areas", views.AreaViewSet, basename="areas")
router.register("announcements", views.AnnouncementViewSet, basename="announcements")

urlpatterns = []

urlpatterns += router.urls
