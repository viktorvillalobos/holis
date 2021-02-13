import pytest

from . import recipes


@pytest.fixture
def active_user():
    return recipes.generic_user.make()


@pytest.fixture
def generate_project_and_user():
    def _():
        project = recipes.generic_company_project.make()
        user = recipes.generic_user.make(company=project.company)

        return project, user

    return _


@pytest.fixture
def generate_projects_and_user():
    def _(kind: int, quantity: int = 1):
        company = recipes.generic_company.make()
        user = recipes.generic_user.make(company=company)
        projects = recipes.generic_normal_project.make(
            kind=kind, company=company, members=[user], _quantity=quantity
        )

        return projects, user

    return _
