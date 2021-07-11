from django.conf import settings
from django.urls import include, path

urlpatterns = [path("v100/", include("apps.chat.api.v100.urls"))]
