from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Rest API for the app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="viktor@adslab.io"),
        license=openapi.License(name="Private License"),
    )
)


class HealtAPIVIew(APIView):
    permission_classes = []

    def get(self, request, format=None):
        return Response(status=200)


app_name = "api"
urlpatterns = [
    path("healthcheck/", HealtAPIVIew.as_view(), name="healthcheck"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("core/", include("apps.core.api.urls")),
    path("users/", include(("apps.users.api.urls", "users"), namespace="users")),
    path("chat/", include(("apps.chat.api.urls", "chat"), namespace="chat")),
    path(
        "projects/",
        include(("apps.projects.api.urls", "projects"), namespace="projects"),
    ),
    path("web/", include(("apps.web.api.urls", "web"), namespace="web")),
]
