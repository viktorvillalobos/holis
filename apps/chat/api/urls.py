from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.chat.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("channels", views.ChannelViewSet, basename="channels")

urlpatterns = [
    path(
        "get-or-create-room/",
        views.GetOrCreateRoomAPIView.as_view(),
        name="get-or-create-room",
    ),
    path(
        "get-turn-credentials/",
        views.GetTurnCredentialsAPIView.as_view(),
        name="get-turn-credentials",
    ),
    path("recents/", views.RecentChatsAPIView.as_view(), name="recents"),
    path(
        "room/<uuid:room_uuid>/messages/",
        views.MessageListAPIView.as_view(),
        name="message-list",
    ),
    path(
        "room/<uuid:room_uuid>/messages/new-with-attachments/",
        views.UploadFileAPIView.as_view(),
        name="message-with-attachments",
    ),
]

urlpatterns += router.urls
