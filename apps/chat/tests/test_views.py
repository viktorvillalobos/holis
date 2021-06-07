from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
import uuid

from apps.chat.models import MessageAttachment
from apps.chat.tests import baker_recipes as chat_recipes
from apps.users.tests import baker_recipes as user_recipes

from ..api import views as chat_views


@pytest.mark.django_db
class TestUploadFileAPIView:
    def setup_method(self, method):
        self.room = chat_recipes.adslab_room_one_to_one.make()
        self.user = user_recipes.user_viktor.make()
        self.kwargs = {"room_uuid": self.room.uuid}
        self.url = reverse("api-v1:chat:message-with-attachments", kwargs=self.kwargs)
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        images = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )

        self.files = [video, images]

    def test_upload_returns_201(
        self,
        mocker,
        expected_chat_upload_file_fields,
        expected_message_raw_with_attachments_fields,
    ):
        mocked_broadcast = mocker.patch(
            "apps.chat.api.views.chat_services.broadcast_chat_message_with_attachments"
        )
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

        mocked_broadcast.assert_called_once_with(
            company_id=self.user.company_id,
            room_uuid=self.room.uuid,
            message_uuid=uuid.UUID(parsed_response["id"]),
        )


@pytest.mark.django_db
class TestRecentChatsAPIView:
    def setup_method(self):
        self.user_viktor = user_recipes.user_viktor.make()
        self.user_julls = user_recipes.user_julls.make()
        self.user_tundi = user_recipes.user_tundi.make()

        self.room_viktor_julls = chat_recipes.adslab_room_one_to_one.make(
            members=[self.user_viktor, self.user_julls]
        )

        self.room_viktor_tundi = chat_recipes.adslab_room_one_to_one.make(
            name="room-viktor-tundi", members=[self.user_viktor, self.user_tundi]
        )
        self.url = reverse("api-v1:chat:recents")

        chat_recipes.adslab_message_one_to_one.make()
        chat_recipes.adslab_message_one_to_one.make(room=self.room_viktor_tundi)

    def test_get_method(self):
        rf = APIRequestFactory()
        request = rf.get(self.url, format="json")
        force_authenticate(request, user=self.user_viktor)

        expected_result = [
            {
                "room": str(self.room_viktor_julls.uuid),
                "avatar_thumb": self.user_julls.avatar_thumb,
                "id": self.user_julls.id,
                "name": self.user_julls.name,
            },
            {
                "room": str(self.room_viktor_tundi.uuid),
                "avatar_thumb": self.user_tundi.avatar_thumb,
                "id": self.user_tundi.id,
                "name": self.user_tundi.name,
            },
        ]

        response = chat_views.RecentChatsAPIView.as_view()(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert response_data == expected_result

    def test_get_method_filtered(self):
        rf = APIRequestFactory()
        request = rf.get(self.url, {"limit": 1}, format="json")
        force_authenticate(request, user=self.user_viktor)

        expected_result = [
            {
                "room": str(self.room_viktor_tundi.uuid),
                "avatar_thumb": self.user_tundi.avatar_thumb,
                "id": self.user_tundi.id,
                "name": self.user_tundi.name,
            }
        ]

        response = chat_views.RecentChatsAPIView.as_view()(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)
        assert response_data == expected_result
