from apps.web import views
from django.urls import path
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    path("", views.SoonTemplateView.as_view(), name="soon",),
    path(
        "check-company/",
        views.CheckCompanyView.as_view(),
        name="check-company",
    ),
    path("login/", views.LoginView.as_view(), name="login",),
    path("start-pwa/", views.PWAView.as_view(), name="start-pwa",),
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
    path("signup/step1/", views.SignUpStep1.as_view(), name="signup-step-1",),
    path("signup/step2/", views.SignUpStep2.as_view(), name="signup-step-2",),
    path(
        "signup/step3/<uuid:pk>/",
        views.SignUpStep3.as_view(),
        name="signup-step-3",
    ),
    path(
        "signup/step4/<uuid:pk>/",
        views.SignUpStep4.as_view(),
        name="signup-step-4",
    ),
    path(
        "signup/step5/<uuid:pk>/",
        views.SignUpStep5.as_view(),
        name="signup-step-5",
    ),
    path("logout", views.logout_view, name="logout"),
]
