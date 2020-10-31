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


class MessageSerializer(serializers.ModelSerializer):
    """
    WARNING: This is used by Consumers.
    """

    avatar_thumb = serializers.CharField(source="user.avatar_thumb")
    user_name = serializers.CharField(source="user.name")
    user_id = serializers.CharField(source="user.id")

    class Meta:
        model = chat_models.Message
        fields = (
            "id",
            "created",
            "avatar_thumb",
            "text",
            "room",
            "user_id",
            "user_name",
        )
        read_only_fields = fields
