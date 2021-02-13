from django.urls import reverse

import pytest

from ..lib import constants as projects_constants
from ..models import Project


@pytest.mark.django_db
def test_get_company_project_view_by_company_id(client, generate_project_and_user):
    project, user = generate_project_and_user()
    url = reverse("api-v1:projects:get_company_project_by_company_id_view")
    client.force_login(user)
    response = client.get(url)

    assert Project.objects.count() == 1
    assert user.company_id == project.company_id
    assert response.status_code == 200
    assert response.json()["uuid"] == str(project.uuid)


@pytest.mark.django_db
def test_get_project_by_kind_view(client, generate_projects_and_user):
    projects, user = generate_projects_and_user(
        kind=projects_constants.ProjectKind.PROJECT.value, quantity=3
    )

    url = reverse(
        "api-v1:projects:get_projects_by_kind_view",
        args=(projects_constants.ProjectKind.PROJECT.value,),
    )
    client.force_login(user)
    response = client.get(url)
    data = response.json()

    expected_project_uuids = [project.uuid for project in projects]
    assert response.status_code == 200
    assert "results" in data

    for project_dict in data["results"]:
        project_dict["uuid"] in expected_project_uuids
