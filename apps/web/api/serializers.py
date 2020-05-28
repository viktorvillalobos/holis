from rest_framework import serializers


class GetEarlyAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()
    origin = serializers.CharField()
