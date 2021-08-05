from typing import Union

from uuid import UUID

from apps.projects.context.models import Task
from apps.projects.lib.exceptions import TaskDoesNotExist

from .context.providers import task as task_providers


def delete_task_by_uuid(
    company_id: int, project_uuid: Union[UUID, str], task_uuid: Union[UUID, str]
) -> None:
    try:
        task_providers.delete_task_by_company_and_uuid(
            company_id=company_id, project_uuid=project_uuid, task_uuid=task_uuid
        )
    except Task.DoesNotExist:
        raise TaskDoesNotExist
