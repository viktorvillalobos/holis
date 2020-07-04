from django.urls import path
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/soon.html"), name="home"),
    path("before/", TemplateView.as_view(template_name="pages/home.html"), name="homeBefore"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about",
    ),
]
