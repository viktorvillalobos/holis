from typing import Any, Union

import datetime
from uuid import uuid4

from ..models import Task


def get_tasks_by_project_uuid(project_uuid: Union[str, uuid4]) -> list[Task]:
    return Task.objects.filter(project_uuid=project_uuid).order_by("created")


def create_task_by_data(
    company_id: int,
    project_uuid: Union[str, uuid4],
    assigned_to_id: int,
    title: str,
    content: str,
    created_by_id: int,
    due_date: datetime.date,
) -> Task:

    return Task.objects.create(
        company_id=company_id,
        project_uuid=project_uuid,
        assigned_to_id=assigned_to_id,
        title=title,
        content=content,
        created_by_id=created_by_id,
        due_date=due_date,
    )
