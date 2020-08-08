from rest_framework import serializers

from apps.users import models as user_models
from apps.chat import models as chat_models


class GetOrCreateRoomSerializer(serializers.Serializer):
    members = serializers.ListField(child=serializers.CharField())
    many = serializers.BooleanField(default=False)


class RecentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ("name", "jid", "avatar_thumb")
