from apps.web import views
from django.urls import path
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", views.SoonTemplateView.as_view(), name="soon",),
    path(
        "before/",
        TemplateView.as_view(template_name="pages/home.html"),
        name="homeBefore",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="homeBefore",
    ),
]
