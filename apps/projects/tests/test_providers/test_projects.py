import pytest

from ...lib import constants as projects_constants
from ...models import Project
from ...providers import project as project_providers
from .. import recipes as project_recipes


@pytest.mark.django_db
def test_get_or_create_company_project_by_company_id(django_assert_num_queries):
    project = project_recipes.generic_company_project.make()

    with django_assert_num_queries(1):
        result, _ = project_providers.get_or_create_company_project_by_company_id(
            company_id=project.company_id
        )


@pytest.mark.django_db
def test_get_or_create_company_project_by_company_id():
    project = project_recipes.generic_company_project.make()

    result, _ = project_providers.get_or_create_company_project_by_company_id(
        company_id=project.company_id
    )


@pytest.mark.django_db
def test_get_or_create_company_project_by_company_id(django_assert_num_queries):
    project = project_recipes.generic_company_project.make()

    with django_assert_num_queries(1):
        result, _ = project_providers.get_or_create_company_project_by_company_id(
            company_id=project.company_id
        )

    assert Project.objects.count() == 1
    assert result.uuid == project.uuid
    assert result.name == project.name


@pytest.mark.django_db
def test_get_projects_by_user_id_and_kind(django_assert_num_queries):
    user1 = project_recipes.generic_user.make(email="john@doe.com")
    user2 = project_recipes.generic_user.make(email="doe@john.com")
    generic_normal_projects = project_recipes.generic_normal_project.make(
        members=(user1, user2), _quantity=3
    )

    with django_assert_num_queries(1):
        results = list(
            project_providers.get_projects_by_user_id_and_kind(
                user_id=user1.id, kind=projects_constants.ProjectKind.PROJECT.value
            )
        )

    expected_results_uuid = [project.uuid for project in generic_normal_projects]

    assert len(results) == 3

    for project in results:
        assert isinstance(project, Project)
        assert project.uuid in expected_results_uuid


@pytest.mark.django_db
def test_create_project_by_company_and_user_id(django_assert_num_queries):
    user = project_recipes.generic_user.make(email="john@doe.com")

    with django_assert_num_queries(2):
        instance = project_providers.create_project_by_company_and_user_id(
            company_id=user.company_id, user_id=user.id, kind=3, name="DEMO-PROJECT"
        )

    assert instance.name == "DEMO-PROJECT"
