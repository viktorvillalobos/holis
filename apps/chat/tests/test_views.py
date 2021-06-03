from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
import uuid
from freezegun import freeze_time

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


# @freeze_time("2016-03-28 14:32:00", tz_offset=-4)
@pytest.mark.django_db
def test_message_list_api_view():

    user = user_recipes.user_viktor.make()
    room_read = chat_recipes.adslab_room_one_to_one_room_read.make(user_id=user.id)
    room = room_read.room
    url = reverse("api-v1:chat:message-list", args=(room.uuid,))

    for i in range(10):
        chat_recipes.adslab_message_one_to_one.make(room=room, text=f"message-{i}")

    rf = APIRequestFactory()
    request = rf.get(url, format="json")

    force_authenticate(request, user=user)

    response = chat_views.MessageListAPIView.as_view()(
        request, room_uuid=room.uuid
    ).render()

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)

    expected_fields = {"results", "next", "previous", "last_read_timestamp"}

    for field in expected_fields:
        assert field in response_data

    assert response_data["last_read_timestamp"] == room_read.timestamp.isoformat()

    assert len(response_data["results"]) == 10

    last_message = response_data["results"][-1]

    assert last_message["text"] == "message-9"
