from typing import Any, Callable

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from apps.utils.pagination import paginate_response

from ..lib import constants as projects_constants
from ..providers import project as project_providers
from . import serializers


@api_view(["GET"])
def get_company_project_by_company_id_view(request: Request) -> Response:
    project, _ = project_providers.get_or_create_company_project_by_company_id(
        company_id=request.user.company_id
    )

    serialized_data = serializers.ProjectSerializer(project).data
    return Response(serialized_data, status.HTTP_200_OK)


@api_view(["GET"])
def get_projects_by_kind_view(request: Request, project_kind_value: int) -> Response:

    allowed_values = [str(value) for value in projects_constants.ProjectKind.values]

    if project_kind_value not in allowed_values:
        raise ValidationError(
            "Invalid project kind value %(value)s", params={"value": project_kind_value}
        )

    projects = project_providers.get_projects_by_user_id_and_kind(
        user_id=request.user.id, kind=project_kind_value
    )

    return paginate_response(
        queryset=projects,
        request=request,
        serializer_class=serializers.ProjectSerializer,
    )
