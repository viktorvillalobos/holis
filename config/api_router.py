from django.urls import include, path


app_name = "api"
urlpatterns = [
    path("", include("apps.core.api.urls")),
    path("", include("apps.users.api.urls")),
]
