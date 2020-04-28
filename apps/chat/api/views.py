from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from apps.chat import models
from apps.chat.api import serializers


class ChannelViewSet(ModelViewSet):
    serializer_class = serializers.ChannelSerializer
    queryset = models.Channel.objects.all()

    def get_queryset(self):
        return self.queryset.filter(company__id=self.request.user.company_id)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk):
        channel = self.get_object()
        serializer = serializers.MessageSerializer(
            channel.messages.all(), many=True
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)
