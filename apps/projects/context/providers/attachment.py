from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet

from uuid import UUID

from ...context.models import Attachment


def create_attachments_by_project_uuid(
    company_id: int, project_uuid: UUID, files: list[InMemoryUploadedFile]
) -> list[Attachment]:
    attachments = [
        Attachment(
            company_id=company_id,
            project_uuid=project_uuid,
            file=_file,
            mime=_file.content_type,
        )
        for _file in files
    ]

    created_messages = Attachment.objects.bulk_create(attachments)

    return created_messages


def get_attachments_by_project_uuid(
    company_id: int, project_uuid: Union[UUID, str]
) -> QuerySet:
    return Attachment.objects.filter(company_id=company_id, project_uuid=project_uuid)
