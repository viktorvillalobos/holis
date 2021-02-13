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
