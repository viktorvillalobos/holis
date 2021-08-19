from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    path("get-or-create-room/", views.GetOrCreateConversationRoomAPIView.as_view()),
    path("get-turn-credentials/", views.GetTurnCredentialsAPIView.as_view()),
    path("room/recents/", views.RecentRoomsAPIView.as_view(), name="recents"),
    path("room/<uuid:room_uuid>/", views.RoomViewSet.as_view({"get": "retrieve"})),
    path(
        "room/<uuid:room_uuid>/exit",
        views.RoomViewSet.as_view({"post": "exit"}),
        name="room-exit",
    ),
    path(
        "room/<uuid:room_uuid>/upload-image/",
        views.UploadRoomImageViewSet.as_view({"post": "create"}),
        name="upload-room-image",
    ),
    path("room/<uuid:room_uuid>/messages/", views.MessageListAPIView.as_view()),
    path(
        "room/<uuid:room_uuid>/messages/new-with-attachments/",
        views.UploadFileAPIView.as_view(),
        name="message-with-attachments",
    ),
]

urlpatterns += router.urls
