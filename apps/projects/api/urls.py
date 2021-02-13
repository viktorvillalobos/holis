from django.urls import path

from . import views

urlpatterns = [
    path(
        "company/",
        views.get_company_project_view_by_company_id,
        name="get_company_project_view_by_company_id",
    )
]
