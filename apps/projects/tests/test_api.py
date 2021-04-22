from typing import Optional

from django.urls import reverse
from django.utils import timezone

import json
import pytest
import uuid
from datetime import timedelta
from model_bakery import baker

from apps.users.tests import baker_recipes as user_recipes

from ..lib import constants as projects_constants
from ..models import Project
from ..tests import recipes as project_recipes


def is_valid_uuid(val: str) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


def is_valid_uuid(val: str) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


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
        "api-v1:projects:project_resource",
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


@pytest.mark.django_db
def test_create_normal_project(client):
    active_user = user_recipes.user_viktor.make()
    expected_kind = projects_constants.ProjectKind.PROJECT.value
    url = reverse("api-v1:projects:project_resource", args=(expected_kind,))

    client.force_login(active_user)

    start_date = timezone.now().date().isoformat()
    end_date = (timezone.now().date() + timedelta(days=15)).isoformat()

    expected_data = dict(
        name="MY-NORMAL-PROJECT",
        company_id=active_user.company_id,
        description="my-custom-description",
        start_date=start_date,
        end_date=end_date,
    )
    requested_data = json.dumps(expected_data)

    response = client.post(url, data=requested_data, content_type="application/json")
    data = response.json()

    assert response.status_code == 201
    assert Project.objects.count() == 1
    assert data["name"] == expected_data["name"]
    assert data["company_id"] == expected_data["company_id"]
    assert data["description"] == "my-custom-description"
    assert data["start_date"] == start_date
    assert data["end_date"] == end_date
    assert is_valid_uuid(data["uuid"])
    assert active_user.id == data["members"][0]["id"]
    assert active_user.name == data["members"][0]["name"]


@pytest.mark.django_db(transaction=True)
def test_create_tasks(client):
    project = project_recipes.generic_company_project.make()
    active_user = user_recipes.user_viktor.make(company_id=project.company_id)

    url = reverse("api-v1:projects:task_resource", args=(project.uuid,))

    client.force_login(active_user)

    expected_due_date = timezone.now().date().isoformat()

    assert active_user.company_id == project.company_id

    expected_data = dict(
        project_uuid=str(project.uuid),
        company_id=project.company_id,
        assigned_to=active_user.id,
        due_data=expected_due_date,
        title="my-custom-title",
        content="my-custom-content",
    )

    requested_data = json.dumps(expected_data)

    response = client.post(url, data=requested_data, content_type="application/json")
    data = response.json()

    assert response.status_code == 201

    for key in expected_data.keys():
        data[key] == expected_data[key]


@pytest.mark.django_db(transaction=True)
def test_get_tasks_by_project_view(client):
    project = project_recipes.generic_company_project.make()
    active_user = user_recipes.user_viktor.make(company_id=project.company_id)
    task = baker.make("projects.Task", project=project)

    url = reverse("api-v1:projects:task_resource", args=(project.uuid,))

    client.force_login(active_user)
    response = client.get(url, content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) == 1

    assert str(task.uuid) == data["results"][0]["uuid"]
