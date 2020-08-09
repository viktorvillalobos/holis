from rest_framework import serializers

from apps.chat.uc import RoomCreate
from apps.users import models as user_models
from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    to = serializers.CharField()


class RecentsSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()

    def get_room(self, obj):
        uc = RoomCreate(
            obj.company, [obj.id, self.context["request"].user.id]
        )
        return uc.execute().get_room().id

    class Meta:
        model = user_models.User
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
