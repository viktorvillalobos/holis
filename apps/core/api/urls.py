from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.core.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("companies", views.CompanyViewSet, basename="companies")
router.register("areas", views.AreaViewSet, basename="areas")
router.register("announcements", views.AnnouncementViewSet, basename="announcements")
router.register("changelogs", views.ChangeLogViewSet, basename="changelogs")

urlpatterns = []

urlpatterns += router.urls
