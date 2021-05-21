from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest

from apps.chat.models import MessageAttachment
from apps.chat.tests import baker_recipes as chat_recipes
from apps.users.tests import baker_recipes as user_recipes

from ..api import views as chat_views


@pytest.mark.django_db
class TestUploadFileAPIView:
    def setup_method(self, method):
        self.room = chat_recipes.adslab_room_one_to_one.make()
        self.user = user_recipes.user_viktor.make()
        self.kwargs = {"room_uuid": self.room.id}
        self.url = reverse("api-v1:chat:message-with-attachments", kwargs=self.kwargs)
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        images = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )

        self.files = [video, images]

    def test_upload_returns_204(
        self,
        expected_chat_upload_file_fields,
        expected_message_raw_with_attachments_fields,
    ):
        rf = APIRequestFactory()
        request = rf.post(
            self.url,
            data={"files": self.files, "text": "This is a message"},
            format="multipart",
        )

        force_authenticate(request, user=self.user)

        response = chat_views.UploadFileAPIView.as_view()(
            request, **self.kwargs
        ).render()

        assert response.status_code == status.HTTP_201_CREATED

        parsed_response = json.loads(response.content)

        for field in expected_message_raw_with_attachments_fields:
            assert field in parsed_response

        attachment_datas = parsed_response["attachments"]
        assert len(attachment_datas) == 2

        assert MessageAttachment.objects.count() == 2

        for attachment_data in attachment_datas:
            for field in expected_chat_upload_file_fields:
                assert field in attachment_data
