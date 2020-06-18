from apps.chat import models
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = "__all__"


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageAttachment
        fields = ["attachment", "mimetype", "created"]


class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = models.Message
        fields = "__all__"


class GetOrCreateChannelSerializer(serializers.Serializer):
    members = serializers.ListField(child=serializers.CharField())
