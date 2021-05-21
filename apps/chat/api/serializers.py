from rest_framework import serializers

from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    to = serializers.CharField()


class RecentsSerializer(serializers.ModelSerializer):
    room = serializers.UUIDField(source="id")
    avatar_thumb = serializers.SerializerMethodField()

    def get_avatar_thumb(self, obj):
        return (
            obj.members.exclude(id=self.context["request"].user.id).first().avatar_thumb
        )

    class Meta:
        model = chat_models.Room
        fields = ("name", "id", "room", "avatar_thumb")
        read_only_fields = fields


class MessageRawSerializer(serializers.Serializer):
    avatar_thumb = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    id = serializers.CharField()
    room = serializers.UUIDField()
    created = serializers.DateTimeField()
    text = serializers.CharField()
    room = serializers.CharField()

    def get_avatar_thumb(self, obj: chat_models.Message) -> str:
        return obj.user.avatar_thumb

    def get_user_name(self, obj: chat_models.Message) -> str:
        return obj.user.name

    def get_user_id(self, obj: chat_models.Message) -> int:
        return obj.user_id


class MessageAttachmentChatSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    company_id = serializers.IntegerField()
    message_uuid = serializers.UUIDField(source="message.pk")
    room_uuid = serializers.UUIDField(source="message.room_id")
    user_id = serializers.IntegerField(source="message.user.id")
    user_name = serializers.CharField(source="message.user.name")
    attachment_url = serializers.CharField(source="attachment.url")
    attachment_mimetype = serializers.CharField(source="mimetype")


class MessageWithAttachmentsSerializer(MessageRawSerializer):
    attachments = MessageAttachmentChatSerializer(many=True)
