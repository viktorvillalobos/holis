from rest_framework import serializers

from apps.users import models as user_models
from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    to = serializers.CharField()


class RecentsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    id = serializers.CharField(source="user.id")
    avatar_thumb = serializers.CharField(source="user.avatar_thumb")

    class Meta:
        model = chat_models.Message
        fields = ("name", "id", "avatar_thumb", "room")


class MessageSerializer(serializers.ModelSerializer):
    """
        WARNING: This is used by Consumers.
    """
    avatar_thumb = serializers.CharField(source="user.avatar_thumb")
    user_name = serializers.CharField(source="user.name")

    class Meta:
        model = chat_models.Message
        fields = '__all__'
