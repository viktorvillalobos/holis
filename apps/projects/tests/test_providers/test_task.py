from django.db.models import Manager
from django.utils import timezone

import pytest
from uuid import uuid4

from ...context.models import Task
from ...context.providers import task as task_providers
from .. import baker_recipes as project_recipes


def test_create_task_by_data(mocker):
    mocked_task = mocker.patch("apps.projects.context.providers.task.Task", spec=Task)
    mocked_provider = mocker.patch(
        "apps.projects.context.providers.task.get_tasks_count_by_company_and_project_uuid"
    )
    mocked_provider.return_value = 1

    project_uuid = uuid4()
    args = dict(
        company_id=123,
        project_uuid=project_uuid,
        title="my-task-title",
        content="my-task-content",
        created_by_id=456,
        due_date=timezone.now().date(),
        assigned_to_id=1,
        is_done=True,
    )

    task_providers.create_task_by_data(**args)

    mocked_provider.assert_called_once_with(company_id=123, project_uuid=project_uuid)
    mocked_task.objects.create.assert_called_once_with(index=1, **args)


@pytest.mark.django_db
def test_move_task_by_task_uuid():
    company = project_recipes.generic_company.make()
    tasks = [
        project_recipes.generic_normal_task.make(index=index, company=company)
        for index in range(3)
    ]

    assert [task.index for task in tasks] == [0, 1, 2]

    expected_result = [tasks[0].uuid, tasks[2].uuid, tasks[1].uuid]

    task_to_move = tasks[2]

    result = task_providers.move_task_by_task_uuid_and_above_index(
        company_id=task_to_move.company_id,
        project_uuid=task_to_move.project_uuid,
        task_uuid=task_to_move.uuid,
        to_index=1,
    )

    result = [task.uuid for task in result]
    assert expected_result == result


def test_bulk_create_tasks_by_dataclasses(mocker):
    mocked_class = mocker.patch("apps.projects.context.providers.task.Task")

    to_create_task_fake = [1, 2, 3]
    task_providers.bulk_create_tasks_by_dataclasses(to_create_tasks=to_create_task_fake)

    mocked_class.objects.bulk_create.assert_called_once_with(to_create_task_fake)


def test_get_task_by_uuid(mocker):
    mocked_class = mocker.patch("apps.projects.context.providers.task.Task")

    expected_uuid = uuid4()
    expected_company_id = 123
    task_providers.get_task_by_company_and_uuid(
        company_id=expected_company_id, task_uuid=expected_uuid
    )

    mocked_class.objects.get.assert_called_once_with(
        company_id=expected_company_id, uuid=expected_uuid
    )
