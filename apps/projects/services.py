from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile

from uuid import UUID

from apps.projects.context.models import Task
from apps.projects.lib.exceptions import TaskDoesNotExist
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .context.providers import attachment as attachment_providers
from .context.providers import task as task_providers
from .lib.dataclasses import AttachmentData


def delete_task_by_uuid(
    company_id: int, project_uuid: Union[UUID, str], task_uuid: Union[UUID, str]
) -> None:
    try:
        task_providers.delete_task_by_company_and_uuid(
            company_id=company_id, project_uuid=project_uuid, task_uuid=task_uuid
        )
    except Task.DoesNotExist:
        raise TaskDoesNotExist


def create_attachment_by_project_uuid(
    company_id: int, project_uuid: Union[UUID, str], files: list[InMemoryUploadedFile]
) -> list[AttachmentData]:
    attachments = attachment_providers.create_attachment_by_project_uuid(
        company_id=company_id, project_uuid=project_uuid, files=files
    )

    return [
        build_dataclass_from_model_instance(klass=AttachmentData, instance=attachment)
        for attachment in attachments
    ]


def get_attachments_by_project_uuid(
    company_id: int, project_uuid: Union[UUID, str]
) -> list[AttachmentData]:
    attachments = attachment_providers.get_attachments_by_project_uuid(
        company_id=company_id, project_uuid=project_uuid
    )

    return [
        build_dataclass_from_model_instance(klass=AttachmentData, instance=attachment)
        for attachment in attachments
    ]
