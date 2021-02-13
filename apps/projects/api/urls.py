from django.urls import path

from . import views

urlpatterns = [
    path(
        "company/",
        views.get_company_project_by_company_id_view,
        name="get_company_project_by_company_id_view",
    ),
    path(
        "kind/<str:project_kind_value>/",
        views.get_projects_by_kind_view,
        name="get_projects_by_kind_view",
    ),
]
