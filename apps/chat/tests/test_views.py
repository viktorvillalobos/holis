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
        self.user = user_recipes.user_viktor.make()
        self.message = chat_recipes.adslab_message_one_to_one.make(
            company=self.user.company
        )
        self.kwargs = {
            "message_uuid": self.message.id,
            "room_uuid": self.message.room_id,
        }
        self.url = reverse("api-v1:chat:upload-file", kwargs=self.kwargs)
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        images = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )

        self.files = [video, images]

    def test_upload_returns_204(self, expected_chat_upload_file_fields):
        rf = APIRequestFactory()
        request = rf.put(self.url, data={"files": self.files}, format="multipart")

        force_authenticate(request, user=self.user)

        response = chat_views.UploadFileAPIView.as_view()(
            request, **self.kwargs
        ).render()

        assert response.status_code == status.HTTP_204_NO_CONTENT

        parsed_response = json.loads(response.content)
        assert len(parsed_response) == 2

        assert MessageAttachment.objects.count() == 2

        for attachment_data in parsed_response:
            assert str(self.message.pk) == attachment_data["message_uuid"]
            for field in expected_chat_upload_file_fields:
                assert field in attachment_data
