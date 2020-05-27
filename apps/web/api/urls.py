from django.urls import path

from apps.web.api import views


urlpatterns = [
    path(
        "get-early-access/",
        views.GetEarlyAccessAPIView.as_view(),
        name="get-early-access",
    )
]
