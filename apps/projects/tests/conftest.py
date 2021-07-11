import pytest

from . import baker_recipes


@pytest.fixture
def active_user():
    return baker_recipes.generic_user.make()


@pytest.fixture
def generate_project_and_user():
    def _():
        project = baker_recipes.generic_company_project.make()
        user = baker_recipes.generic_user.make(company=project.company)

        return project, user

    return _


@pytest.fixture
def generate_projects_and_user():
    def _(kind: int, quantity: int = 1):
        company = baker_recipes.generic_company.make()
        user = baker_recipes.generic_user.make(company=company)
        projects = baker_recipes.generic_normal_project.make(
            kind=kind, company=company, members=[user], _quantity=quantity
        )

        return projects, user

    return _
