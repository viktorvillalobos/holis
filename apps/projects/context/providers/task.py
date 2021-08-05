from typing import Any, Dict, Optional, Union

from django.db.models import Max

import datetime
from uuid import UUID, uuid4

from ...lib.exceptions import TaskDoesNotExist
from ..models import Task


def get_tasks_by_project_uuid(project_uuid: Union[str, UUID]) -> list[Task]:
    return Task.objects.filter(project_uuid=project_uuid).order_by("index")


def get_tasks_count_by_company_and_project_uuid(
    company_id: int, project_uuid: Union[str, UUID]
) -> int:
    return Task.objects.filter(company_id=company_id, project_uuid=project_uuid).count()


def create_task_by_data(
    company_id: int,
    project_uuid: Union[str, UUID],
    title: str,
    content: Optional[str],
    created_by_id: int,
    due_date: Optional[datetime.date] = None,
    assigned_to_id: Optional[int] = None,
    is_done: bool = False,
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
        is_done=is_done,
    )


def update_task_by_data(
    company_id: int,
    project_uuid: Union[str, UUID],
    task_uuid: Union[str, UUID],
    title: str,
    content: Optional[str],
    created_by_id: int,
    due_date: Optional[datetime.date] = None,
    assigned_to_id: Optional[int] = None,
    index: Optional[int] = None,
    is_done: bool = False,
) -> Task:

    if not index:
        index = get_tasks_count_by_company_and_project_uuid(
            company_id=company_id, project_uuid=project_uuid
        )

    task_to_update = Task.objects.get(
        company_id=company_id, project_uuid=project_uuid, uuid=task_uuid
    )
    task_to_update.title = title
    task_to_update.content = content
    task_to_update.created_by_id = created_by_id
    task_to_update.due_date = due_date
    task_to_update.index = index
    task_to_update.assigned_to_id = assigned_to_id
    task_to_update.is_done = is_done

    task_to_update.save()

    return task_to_update


def move_task_by_task_uuid_and_above_index(
    company_id: int,
    project_uuid: Union[str, UUID],
    task_uuid: Union[str, UUID],
    to_index: Optional[int] = None,
) -> list[Task]:

    # Get tasks ordered by index
    tasks_of_the_project = list(
        Task.objects.filter(company_id=company_id, project_uuid=project_uuid).order_by(
            "index"
        )
    )

    # Find the task to move
    task_to_move = [task for task in tasks_of_the_project if task.uuid == task_uuid][0]
    task_to_move_index = tasks_of_the_project.index(task_to_move)

    # Add the task in the new index
    tasks_of_the_project.pop(task_to_move_index)
    tasks_of_the_project.insert(to_index, task_to_move)

    # Update databases indexes
    for index, task in enumerate(tasks_of_the_project):
        task.index = index

    Task.objects.bulk_update(tasks_of_the_project, ["index"])

    return tasks_of_the_project


def bulk_create_tasks_by_dataclasses(to_create_tasks: list[Task]) -> list[Task]:
    return Task.objects.bulk_create(to_create_tasks)


def get_task_by_company_and_uuid(company_id: int, task_uuid: Union[str, UUID]) -> Task:
    try:
        return Task.objects.get(company_id=company_id, uuid=task_uuid)
    except Task.DoesNotExist:
        raise TaskDoesNotExist


def delete_task_by_company_and_uuid(
    company_id: int, task_uuid: Union[str, UUID]
) -> None:
    try:
        Task.objects.get(company_id=company_id, uuid=task_uuid).delete()
    except Task.DoesNotExist:
        raise TaskDoesNotExist


def partial_update_task_by_data(instance: Task, validated_data: Dict[str, Any]) -> Task:
    """
        Allow partial update , this should only be called inside a serializer
    """

    # TODO: [SECURITY] This function should be replaced for something more secure
    # This should on

    for key, value in validated_data.items():
        setattr(instance, key, value)
        instance.save()

    return instance
