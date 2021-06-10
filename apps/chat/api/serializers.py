from django.conf import settings
from rest_framework import serializers

import os

from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    to = serializers.CharField()


class RecentsSerializer(serializers.ModelSerializer):
    room = serializers.UUIDField(source="uuid")
    # This is for legacy compantibilty.
    id = serializers.UUIDField(source="uuid")
    avatar_thumb = serializers.SerializerMethodField()

    def get_avatar_thumb(self, obj):
        return (
            obj.members.exclude(id=self.context["request"].user.id).first().avatar_thumb
        )

    class Meta:
        model = chat_models.Room
        fields = ("name", "uuid", "id", "room", "avatar_thumb")
        read_only_fields = fields


class MessageRawSerializer(serializers.Serializer):
    avatar_thumb = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    uuid = serializers.CharField()
    id = serializers.CharField(source="uuid")
    room = serializers.UUIDField()
    created = serializers.DateTimeField()
    text = serializers.CharField()
    room = serializers.CharField()
    is_readed = serializers.BooleanField(default=False)

    def get_avatar_thumb(self, obj: chat_models.Message) -> str:
        return obj.user.avatar_thumb

    def get_user_name(self, obj: chat_models.Message) -> str:
        return obj.user.name

    def get_user_id(self, obj: chat_models.Message) -> int:
        return obj.user_id


class MessageAttachmentChatSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    id = serializers.UUIDField(source="uuid")
    company_id = serializers.IntegerField()
    message_uuid = serializers.UUIDField(source="message.pk")
    room_uuid = serializers.UUIDField(source="message.room_uuid")
    user_id = serializers.IntegerField(source="message.user.id")
    user_name = serializers.CharField(source="message.user.name")
    attachment_url = serializers.SerializerMethodField()
    attachment_name = serializers.SerializerMethodField()
    attachment_mimetype = serializers.CharField(source="mimetype")

    def get_attachment_url(self, obj):
        if settings.ENVIRONMENT == settings.PRODUCTION:
            return obj.attachment.url

        context = self.context.get("request")
        if context:
            return self.context["request"].build_absolute_uri(obj.attachment.url)

        return f"http://{obj.company.code}.holis.local:8000{obj.attachment.url}"

    def get_attachment_name(self, obj):
        return os.path.basename(obj.attachment.name)


class MessageWithAttachmentsSerializer(MessageRawSerializer):
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return MessageAttachmentChatSerializer(
            obj.attachments.all(), many=True, context=self.context
        ).data
