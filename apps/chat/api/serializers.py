from rest_framework import serializers
from apps.chat import models


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