from apps.web.api import views
from django.urls import path

urlpatterns = [
    path(
        "get-early-access/",
        views.GetEarlyAccessAPIView.as_view(),
        name="get-early-access",
    )
]
