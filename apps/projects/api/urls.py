from django.urls import path

from . import views

urlpatterns = [
    path(
        "company/",
        views.get_company_project_by_company_id_view,
        name="get_company_project_by_company_id_view",
    ),
    path(
        "kind/<str:project_kind_value>", views.project_resource, name="project_resource"
    ),
    path(
        "<uuid:project_uuid>/tasks", views.list_and_create_tasks, name="task_resource"
    ),
    path(
        "<uuid:project_uuid>/tasks/<uuid:task_uuid>",
        views.retrieve_task,
        name="retrieve_task",
    ),
    path(
        "<uuid:project_uuid>/tasks/<uuid:task_uuid>/move/<int:task_index>",
        views.move_task_by_uuid,
        name="move_task_by_uuid",
    ),
]
