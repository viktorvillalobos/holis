from django.urls import include, path

urlpatterns = [path("v100/", include("apps.projects.api.v100.urls"))]
