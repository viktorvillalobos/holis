from django.core.files.uploadedfile import InMemoryUploadedFile

from uuid import UUID

from apps.chat.models import MessageAttachment


def create_message_attachments_by_message_uuid(
    company_id: int, message_uuid: UUID, files: list[InMemoryUploadedFile]
) -> list[MessageAttachment]:
    messages = [
        MessageAttachment(
            company_id=company_id,
            message_id=message_uuid,
            attachment=_file,
            mimetype=_file.content_type,
        )
        for _file in files
    ]

    created_messages = MessageAttachment.objects.bulk_create(messages)

    return created_messages
