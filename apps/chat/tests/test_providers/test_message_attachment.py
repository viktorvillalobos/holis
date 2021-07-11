from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from apps.users.tests import baker_recipes as user_recipes

from ...context.models import MessageAttachment
from ...context.providers import message_attachment as message_attachment_providers
from .. import baker_recipes as chat_recipes


@pytest.mark.django_db
def test_create_message_attachments_by_message_uuid():
    user = user_recipes.user_viktor.make()
    message = chat_recipes.adslab_message_one_to_one.make(company=user.company)
    video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
    image = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")

    message_attachment_providers.create_message_attachments_by_message_uuid(
        company_id=user.company_id, message_uuid=message.pk, files=[video, image]
    )

    attachments = MessageAttachment.objects.all()
    assert len(attachments) == 2
    assert attachments[0].message_uuid == message.uuid
