from typing import Any, Dict

from rest_framework import serializers

from ..models import Project
from ..providers import project as project_providers


class MembersField(serializers.Field):
    def to_representation(self, members):
        return [{"id": member.id, "name": member.name} for member in members.all()]


class ProjectSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, allow_null=True)
    company_id = serializers.IntegerField()
    name = serializers.CharField()
    members = MembersField(required=False, allow_null=True)
    kind = serializers.IntegerField()

    def create(self, validated_data: Dict["str", Any]) -> Project:
        request = self.context["request"]

        project = project_providers.create_project_by_company_and_user_id(
            user_id=request.user.id, **validated_data
        )

        return project
