import pytest

from ...models import Project
from ...providers import project as project_providers
from .. import recipes as project_recipes


@pytest.mark.django_db
def test_get_or_create_company_project_by_company_id():
    project = project_recipes.generic_company_project.make()

    result, _ = project_providers.get_or_create_company_project_by_company_id(
        company_id=project.company_id
    )

    assert Project.objects.count() == 1
    assert result.uuid == project.uuid
    assert result.name == project.name
