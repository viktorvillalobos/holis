from django.urls import path

from . import views

TASKS_URLS = [
    path(
        "<uuid:project_uuid>/tasks/<uuid:task_uuid>",
        views.TaskViewSet.as_view(
            {"get": "retrieve", "patch": "update", "put": "update", "delete": "destroy"}
        ),
        name="update_and_retrieve_task",
    ),
    path(
        "<uuid:project_uuid>/tasks",
        views.TaskViewSet.as_view({"get": "list", "post": "create"}),
        name="task_resource",
    ),
    path(
        "<uuid:project_uuid>/tasks/<uuid:task_uuid>/move/<int:task_index>",
        views.move_task_by_uuid,
        name="move_task_by_uuid",
    ),
]

PROJECT_URLS = [
    path(
        "company/",
        views.get_company_project_by_company_id_view,
        name="get_company_project_by_company_id_view",
    ),
    path(
        "kind/<str:project_kind_value>",
        views.ProjectViewSet.as_view({"get": "list", "post": "create"}),
        name="project_resource",
    ),
    path(
        "<uuid:project_uuid>/attachments/",
        views.ProjectAttachmentAPIView.as_view(),
        name="attachment_resource",
    ),
]

urlpatterns = [*PROJECT_URLS, *TASKS_URLS]
