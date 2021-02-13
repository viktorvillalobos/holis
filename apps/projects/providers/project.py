from typing import Tuple

from django.db.models.query import QuerySet

from ..lib import constants as projects_constants
from ..models import Project


def get_or_create_company_project_by_company_id(
    company_id: int,
) -> Tuple[Project, bool]:

    return Project.objects.get_or_create(
        company_id=company_id,
        kind=projects_constants.ProjectKind.COMPANY.value,
        defaults={"name": f"project-for-{company_id}"},
    )


def get_projects_by_user_id_and_kind(
    user_id: int, kind: projects_constants.ProjectKind
) -> QuerySet:
    return Project.objects.filter(kind=kind, members__id__in=[user_id])
