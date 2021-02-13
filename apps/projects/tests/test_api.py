from django.urls import reverse

import pytest

from ..models import Project
from . import recipes


@pytest.mark.django_db
def test_get_company_project_view_by_company_id(client, generate_project_and_user):
    project, user = generate_project_and_user()
    url = reverse("api-v1:projects:get_company_project_view_by_company_id")
    client.force_login(user)
    response = client.get(url)

    assert Project.objects.count() == 1
    assert user.company_id == project.company_id
    assert response.status_code == 200
    assert response.json()["uuid"] == str(project.uuid)
