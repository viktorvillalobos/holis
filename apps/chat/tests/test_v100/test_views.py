from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
import pytz
import uuid
from freezegun import freeze_time

from apps.users.tests import baker_recipes as user_recipes

from ...api.v100 import serializers
from ...api.v100 import views as chat_views
from ...context.models import MessageAttachment
from ...tests import baker_recipes as chat_recipes


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
            "apps.chat.api.v100.views.chat_services.broadcast_chat_message_with_attachments"
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


@pytest.mark.skip(reason="Flaky")
@pytest.mark.django_db
def test_get_recetents_rooms_api_view():
    user_viktor = user_recipes.user_viktor.make()
    user_julls = user_recipes.user_julls.make()
    user_tundi = user_recipes.user_tundi.make()

    room_viktor_julls = chat_recipes.adslab_room_one_to_one.make(
        members=[user_viktor, user_julls]
    )

    room_viktor_tundi = chat_recipes.adslab_room_one_to_one.make(
        name="room-viktor-tundi", members=[user_viktor, user_tundi]
    )
    url = reverse("api-v1:chat:recents")

    room_viktor_julls_message = chat_recipes.adslab_message_one_to_one.make()
    room_viktor_tundi_message = chat_recipes.adslab_message_one_to_one.make(
        room=room_viktor_tundi
    )

    rf = APIRequestFactory()
    request = rf.get(url, format="json")
    force_authenticate(request, user=user_viktor)

    expected_result = [
        {
            "room": str(room_viktor_julls.uuid),
            "avatar_thumb": user_julls.avatar_thumb,
            "id": user_julls.id,
            "name": user_julls.name,
            "message": room_viktor_julls_message.text,
            # "created": self.room_viktor_julls_message.created
        },
        {
            "room": str(room_viktor_tundi.uuid),
            "avatar_thumb": user_tundi.avatar_thumb,
            "id": user_tundi.id,
            "name": user_tundi.name,
            "message": room_viktor_tundi_message.text,
            # "created": self.room_viktor_tundi_message.created
        },
    ]

    response = chat_views.RecentChatsAPIView.as_view()(request).render()

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)

    # TODO: Find a way to make this right
    for x in response_data:
        x.pop("created")

    assert response_data == expected_result


@pytest.mark.skip(reason="Flaky")
@pytest.mark.django_db(transaction=True)
def test_get_recents_rooms_api_view_filtered():
    user_viktor = user_recipes.user_viktor.make()
    user_julls = user_recipes.user_julls.make()
    user_tundi = user_recipes.user_tundi.make()

    room_viktor_julls = chat_recipes.adslab_room_one_to_one.make(
        members=[user_viktor, user_julls]
    )

    room_viktor_tundi = chat_recipes.adslab_room_one_to_one.make(
        name="room-viktor-tundi", members=[user_viktor, user_tundi]
    )
    url = reverse("api-v1:chat:recents")

    room_viktor_julls_message = chat_recipes.adslab_message_one_to_one.make()
    room_viktor_tundi_message = chat_recipes.adslab_message_one_to_one.make(
        room=room_viktor_tundi
    )

    rf = APIRequestFactory()
    request = rf.get(url, {"limit": 1}, format="json")
    force_authenticate(request, user=user_viktor)

    expected_result = [
        {
            "room": str(room_viktor_tundi.uuid),
            "avatar_thumb": user_tundi.avatar_thumb,
            "id": user_tundi.id,
            "name": user_tundi.name,
            "message": room_viktor_tundi_message.text,
            # "created": self.room_viktor_tundi_message.created,
        }
    ]

    response = chat_views.RecentChatsAPIView.as_view()(request).render()

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)

    # TODO: Find a way to make this right
    for x in response_data:
        x.pop("created")

    assert response_data == expected_result
