from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.core.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = []

urlpatterns += router.urls
