from typing import Any, Callable

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from uuid import uuid4

from apps.utils.pagination import paginate_response

from ..lib import constants as projects_constants
from ..providers import project as project_providers
from ..providers import task as task_providers
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


@api_view(["GET", "POST"])
def project_resource(request: Request, project_kind_value: int) -> Response:
    allowed_values = [str(value) for value in projects_constants.ProjectKind.values]

    if project_kind_value not in allowed_values:
        raise ValidationError(
            "Invalid project kind value %(value)s", params={"value": project_kind_value}
        )

    if request.method == "GET":
        projects = project_providers.get_projects_by_user_id_and_kind(
            user_id=request.user.id, kind=project_kind_value
        )

        return paginate_response(
            queryset=projects,
            request=request,
            serializer_class=serializers.ProjectSerializer,
        )

    serializer = serializers.ProjectSerializer(
        data={"kind": project_kind_value, **request.data}, context={"request": request}
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def task_resource(request: Request, project_uuid: uuid4) -> Response:
    if request.method == "GET":
        tasks = task_providers.get_tasks_by_project_uuid(project_uuid=project_uuid)
        return paginate_response(
            queryset=tasks, request=request, serializer_class=serializers.TaskSerializer
        )

    serializer = serializers.TaskSerializer(
        data={"project_uuid": project_uuid, **request.data},
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def move_task_by_uuid(
    request: Request, project_uuid: uuid4, task_uuid: uuid4, task_index: int
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
