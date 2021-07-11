from typing import Any, Callable

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from uuid import UUID

from apps.utils.pagination import paginate_response

from ...context.providers import project as project_providers
from ...context.providers import task as task_providers
from ...lib import constants as projects_constants
from ...lib.exceptions import TaskDoesNotExist
from . import serializers


@api_view(["GET"])
def get_company_project_by_company_id_view(request: Request) -> Response:
    project, _ = project_providers.get_or_create_company_project_by_company_id(
        company_id=request.user.company_id
    )

    serialized_data = serializers.ProjectSerializer(project).data
    return Response(serialized_data, status.HTTP_200_OK)


def _create_project_by_kind(request: Request, project_kind_value: int) -> Response:
    return Response({"data": project_kind_value}, status=status.HTTP_201_CREATED)


class ProjectViewSet(ViewSet):
    def dispatch(self, *args, **kwargs):
        project_kind_value = kwargs.get("project_kind_value")
        allowed_values = [str(value) for value in projects_constants.ProjectKind.values]

        if project_kind_value not in allowed_values:
            raise ValidationError(
                "Invalid project kind value %(value)s",
                params={"value": project_kind_value},
            )

        return super().dispatch(*args, **kwargs)

    def list(self, request: Request, project_kind_value: int) -> Response:
        projects = project_providers.get_projects_by_company_and_kind(
            company_id=request.user.company_id, kind=project_kind_value
        )

        return paginate_response(
            queryset=projects,
            request=request,
            serializer_class=serializers.ProjectSerializer,
        )

    def create(self, request: Request, project_kind_value: int) -> Response:
        serializer = serializers.ProjectSerializer(
            data={"kind": project_kind_value, **request.data},
            context={"company_id": request.user.company_id, "user_id": request.user.id},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskViewSet(ViewSet):
    def list(self, request, project_uuid: UUID, *args, **kwargs) -> Response:
        tasks = task_providers.get_tasks_by_project_uuid(project_uuid=project_uuid)
        return paginate_response(
            queryset=tasks, request=request, serializer_class=serializers.TaskSerializer
        )

    def create(self, request, project_uuid: UUID, *args, **kwargs) -> Response:
        is_a_bulk_operation = isinstance(request.data, list)

        serializer = serializers.TaskSerializer(
            data=request.data,
            many=is_a_bulk_operation,
            context={
                "user_id": request.user.id,
                "company_id": request.user.company_id,
                "project_uuid": project_uuid,
            },
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(
        self, request, project_uuid: UUID, task_uuid: UUID, *args, **kwargs
    ) -> Response:
        try:
            task = task_providers.get_task_by_company_and_uuid(
                company_id=request.user.company_id, task_uuid=task_uuid
            )
        except TaskDoesNotExist:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(
        self, request, task_uuid: UUID, project_uuid: UUID, *args, **kwargs
    ) -> Response:
        is_partial = request.method == "PATCH"

        task_instance = task_providers.get_task_by_company_and_uuid(
            company_id=self.request.user.company_id, task_uuid=task_uuid
        )

        serializer = serializers.TaskSerializer(
            task_instance,
            data=request.data,
            context={
                "company_id": request.user.company_id,
                "project_uuid": project_uuid,
                "user_id": request.user.id,
            },
            partial=is_partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, project_uuid: UUID, task_uuid: UUID) -> Response:
        try:
            task = task_providers.get_task_by_company_and_uuid(
                company_id=request.user.company_id, task_uuid=task_uuid
            )
        except TaskDoesNotExist:
            raise Http404

        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def move_task_by_uuid(
    request: Request, project_uuid: UUID, task_uuid: UUID, task_index: int
) -> Response:
    result = task_providers.move_task_by_task_uuid_and_above_index(
        company_id=request.user.company_id,
        project_uuid=project_uuid,
        task_uuid=task_uuid,
        to_index=task_index,
    )

    return Response(
        serializers.TaskSerializer(result, many=True).data, status=status.HTTP_200_OK
    )
