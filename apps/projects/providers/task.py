from typing import Any, Optional, Union

from django.db.models import Max

import datetime
from uuid import uuid4

from ..lib.exceptions import TaskDoesNotExist
from ..models import Task


def get_tasks_by_project_uuid(project_uuid: Union[str, uuid4]) -> list[Task]:
    return Task.objects.filter(project_uuid=project_uuid).order_by("index")


def get_tasks_count_by_company_and_project_uuid(
    company_id: int, project_uuid: Union[str, uuid4]
) -> int:
    return Task.objects.filter(company_id=company_id, project_uuid=project_uuid).count()


def create_task_by_data(
    company_id: int,
    project_uuid: Union[str, uuid4],
    title: str,
    content: str,
    created_by_id: int,
    due_date: Optional[datetime.date] = None,
    assigned_to_id: Optional[int] = None,
) -> Task:

    last_task_index = get_tasks_count_by_company_and_project_uuid(
        company_id=company_id, project_uuid=project_uuid
    )

    return Task.objects.create(
        company_id=company_id,
        project_uuid=project_uuid,
        title=title,
        content=content,
        created_by_id=created_by_id,
        due_date=due_date,
        index=last_task_index,
        assigned_to_id=assigned_to_id,
    )


def move_task_by_task_uuid_and_above_index(
    company_id: int,
    project_uuid: Union[str, uuid4],
    task_uuid: Union[str, uuid4],
    to_index: Optional[int] = None,
) -> list[Task]:
    tasks_of_the_project = list(
        Task.objects.filter(company_id=company_id, project_uuid=project_uuid).order_by(
            "index"
        )
    )

    task_to_move = [task for task in tasks_of_the_project if task.uuid == task_uuid][0]
    task_to_move_index = tasks_of_the_project.index(task_to_move)

    tasks_of_the_project.pop(task_to_move_index)
    tasks_of_the_project.insert(to_index, task_to_move)

    return tasks_of_the_project


def bulk_create_tasks_by_dataclasses(to_create_tasks: list[Task]) -> list[Task]:
    return Task.objects.bulk_create(to_create_tasks)


def get_task_by_company_and_uuid(company_id: int, task_uuid: Union[str, uuid4]) -> Task:
    try:
        return Task.objects.get(company_id=company_id, uuid=task_uuid)
    except Task.DoesNotExist:
        raise TaskDoesNotExist
