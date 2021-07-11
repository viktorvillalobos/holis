from django.urls import include, path

urlpatterns = [path("v100/", include("apps.core.api.v100.urls"))]
