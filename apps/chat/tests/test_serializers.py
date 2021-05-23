import pytest

from ..api import serializers
from ..tests import baker_recipes as chat_recipes


@pytest.mark.django_db
def test_recent_serializer(expected_recent_fields, mocker):
    mocker.patch.object(
        serializers.RecentsSerializer,
        "get_avatar_thumb",
        return_value="https://this-custom-url.com",
    )

    room = chat_recipes.adslab_room_one_to_one.make()

    serialized_data = serializers.RecentsSerializer(room).data

    for field in expected_recent_fields:
        assert field in serialized_data

    assert serialized_data["room"] == str(room.id)
    assert serialized_data["id"] == str(room.id)
    assert serialized_data["name"] == room.name


@pytest.mark.django_db
def test_message_raw_serializer(expected_message_raw_fields):
    message = chat_recipes.adslab_message_one_to_one.make()

    serialized_data = serializers.MessageRawSerializer(message).data

    for field in expected_message_raw_fields:
        assert field in expected_message_raw_fields

    assert serialized_data["avatar_thumb"] == message.user.avatar_thumb
    assert serialized_data["user_name"] == message.user.name
    assert serialized_data["user_id"] == message.user.id


@pytest.mark.django_db
def test_message_attachment_serializer(expected_message_attachment_fields, mocker):
    message_attachment = chat_recipes.adslab_attachment_one_to_one.make()

    def build_absolute_uri(obj):
        return message_attachment.attachment.url

    request = mocker.Mock()
    request.build_absolute_uri = build_absolute_uri
    context = {"request": request}

    serialized_data = serializers.MessageAttachmentChatSerializer(
        message_attachment, context=context
    ).data

    for field in expected_message_attachment_fields:
        assert field in expected_message_attachment_fields

    assert serialized_data["message_uuid"] == str(message_attachment.message_id)
    assert serialized_data["room_uuid"] == str(message_attachment.message.room_id)
    assert serialized_data["user_id"] == message_attachment.message.user_id
    assert serialized_data["user_name"] == message_attachment.message.user.name
    assert serialized_data["attachment_url"] == message_attachment.attachment.url
