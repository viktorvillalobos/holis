from django.urls import include, path
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
    ),
)


app_name = "api"
urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc",),
    path("", include("apps.core.api.urls")),
    path("", include("apps.users.api.urls")),
    path("", include("apps.chat.api.urls")),
]
