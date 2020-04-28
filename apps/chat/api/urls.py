from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.chat.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("channels", views.ChannelViewSet, basename="channels")

urlpatterns = []

urlpatterns += router.urls
