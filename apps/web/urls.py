from django.urls import path
from django.views.generic import TemplateView

from apps.web import views

app_name = "web"

urlpatterns = [
    path("soon/", views.SoonTemplateView.as_view(), name="soon"),
    path("check-company/", views.CheckCompanyView.as_view(), name="check-company"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("blog/", views.BlogListView.as_view(), name="blog-list"),
    path("<str:lang_code>/blog/", views.BlogListView.as_view(), name="blog-list"),
    path(
        "blog/<str:cat_slug>/<str:slug>",
        views.BlogSingleView.as_view(),
        name="blog-single",
    ),
    path(
        "<str:lang_code>/blog/<str:cat_slug>/<str:slug>",
        views.BlogSingleView.as_view(),
        name="blog-single",
    ),
    path("", views.HomeView.as_view(), name="home"),
    path("<str:lang_code>/", views.HomeView.as_view(), name="home_with_lang"),
    path(
        "<str:lang_code>/about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("signup/step1/", views.SignUpStep1.as_view(), name="signup-step-1"),
    path("signup/step2/", views.SignUpStep2.as_view(), name="signup-step-2"),
    path("signup/step3/<uuid:pk>/", views.SignUpStep3.as_view(), name="signup-step-3"),
    path("signup/step4/<uuid:pk>/", views.SignUpStep4.as_view(), name="signup-step-4"),
    path("signup/step5/<uuid:pk>/", views.SignUpStep5.as_view(), name="signup-step-5"),
    path("logout", views.logout_view, name="logout"),
    path("<str:slug>/", views.PageSingleView.as_view(), name="page-single"),
]
