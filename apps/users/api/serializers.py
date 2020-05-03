from apps.users import models as users_models
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Status
        fields = ["text", "icon", "is_active"]


class UserSerializer(serializers.ModelSerializer):
    statuses = StatusSerializer(many=True, read_only=True)

    avatar_thumb = serializers.SerializerMethodField()

    def get_avatar_thumb(self, obj):
        if not obj.avatar_thumb:
            return None

        # TODO: This serializer is used in channel consumer
        # this object not have the request object
        # we need to create a converter from scope to request
        # to use drf serlaizers
        try:
            return self.context["request"].build_absolute_uri(obj.avatar_thumb)
        except KeyError:
            return obj.avatar_thumb

    class Meta:
        model = users_models.User
        fields = [
            "id",
            "birthday",
            "company",
            "email",
            "name",
            "position",
            "statuses",
            "username",
            "default_area",
            "avatar",
            "avatar_thumb",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Notification
        fields = "__all__"
