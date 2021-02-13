from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ..providers import project as project_providers
from . import serializers


@api_view(["GET"])
def get_company_project_view_by_company_id(request: Request) -> Response:
    project, _ = project_providers.get_or_create_company_project_by_company_id(
        company_id=request.user.company_id
    )

    serialized_data = serializers.ProjectSerializer(project).data
    return Response(serialized_data, status.HTTP_200_OK)
