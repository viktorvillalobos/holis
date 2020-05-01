from apps.users.api import views
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt import views as jwt_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", views.UserViewSet)
router.register("notifications", views.NotificationViewSet)

urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair",),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh",),
]


urlpatterns += router.urls
