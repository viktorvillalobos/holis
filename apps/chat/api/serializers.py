from rest_framework import serializers

from apps.users import models as user_models
from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    members = serializers.ListField(child=serializers.CharField())
    many = serializers.BooleanField(default=False)


class RecentsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    id = serializers.CharField(source="user.id")
    avatar_thumb = serializers.CharField(source="user.avatar_thumb")

    class Meta:
        model = chat_models.Message
        fields = ("name", "id", "avatar_thumb", "room")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = chat_models.Message
        fields = '__all__'
