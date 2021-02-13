from typing import Tuple

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
