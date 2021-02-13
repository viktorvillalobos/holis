from rest_framework import serializers


class MembersField(serializers.Field):
    def to_representation(self, members):
        return [{"id": member.id, "name": member.name} for member in members.all()]


class ProjectSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    company_id = serializers.IntegerField()
    name = serializers.CharField()
    members = MembersField()
