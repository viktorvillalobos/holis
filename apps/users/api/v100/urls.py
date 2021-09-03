from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from fcm_django.api.rest_framework import FCMDeviceCreateOnlyViewSet

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("profile", views.UserProfileViewSet)
router.register("notifications", views.NotificationViewSet)
router.register("devices", FCMDeviceCreateOnlyViewSet)
router.register("", views.UserViewSet)

urlpatterns = [
    path(
        "me/upload-avatar/", views.UploadAvatarAPIView.as_view(), name="upload-avatar"
    ),
    path("check-company/<str:company_name>/", views.CheckCompanyAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("set-status/", views.SetStatusAPIView.as_view()),
    path(
        "suggest-company-code/",
        views.SuggestCompanyCodeAPIView.as_view(),
        name="suggest-company-code",
    ),
    path("birthdays/", views.BirthdaysViewSet.as_view({"get": "list"})),
    path(
        "invitate/",
        views.UserInvitationViewSet.as_view({"post": "create"}),
        name="invitate",
    ),
]


urlpatterns += router.urls
