from django.urls import path
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about",
    ),
]
