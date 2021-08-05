from typing import Union

from django.core.files.base import File

from dataclasses import dataclass
from uuid import UUID


@dataclass
class ProjectBaseDataClass:
    company_id: int


@dataclass
class AttachmentData(ProjectBaseDataClass):
    project_uuid: Union[UUID, str]
    file: File
    mime: str
