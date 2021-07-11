from django.urls import include, path

urlpatterns = [path("v100/", include("apps.users.api.v100.urls"))]
