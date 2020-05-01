from apps.chat.api import views
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("channels", views.ChannelViewSet, basename="channels")

urlpatterns = []

urlpatterns += router.urls
