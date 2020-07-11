from apps.chat.api import views
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("channels", views.ChannelViewSet, basename="channels")

urlpatterns = [
    # path("get-or-create-channel/", views.GetOrCreateChannelAPIView.as_view()),
    path("get-chat-credentials/", views.GetChatCredentialsAPIView.as_view()),
    path("get-turn-credentials/", views.GetTurnCredentialsAPIView.as_view()),
    path("upload-file/", views.UploadFileAPIView.as_view()),
    path("recents/", views.RecentChatsAPIView.as_view()),
]

urlpatterns += router.urls
