from rest_framework import serializers

from apps.users import models as users_models


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Status
        fields = ["text", "icon", "is_active"]


class UserSerializer(serializers.ModelSerializer):
    statuses = StatusSerializer(many=True, read_only=True)

    class Meta:
        model = users_models.User
        fields = [
            "birthday",
            "company",
            "email",
            "name",
            "position",
            "statuses",
            "url",
            "username",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.Notification
        fields = "__all__"
