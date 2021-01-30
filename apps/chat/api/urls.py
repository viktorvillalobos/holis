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
    path("get-or-create-room/", views.GetOrCreateRoomAPIView.as_view()),
    path("get-turn-credentials/", views.GetTurnCredentialsAPIView.as_view()),
    path("upload-file/", views.UploadFileAPIView.as_view()),
    path("recents/", views.RecentChatsAPIView.as_view()),
    path("room/<uuid:room_uuid>/messages/", views.MessageListAPIView.as_view()),
]

urlpatterns += router.urls
