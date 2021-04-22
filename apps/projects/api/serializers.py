from typing import Any, Dict

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Project, Task
from ..providers import project as project_providers
from ..providers import task as task_providers


class MembersField(serializers.Field):
    def to_representation(self, members):
        return [{"id": member.id, "name": member.name} for member in members.all()]


class UserField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        return {"id": obj.id, "name": obj.name}


class TaskSerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    uuid = serializers.UUIDField(required=False, allow_null=True)
    project_uuid = serializers.UUIDField(required=False, allow_null=True)
    assigned_to = UserField(required=False, allow_null=True)
    due_data = serializers.DateField(required=False, allow_null=True)
    title = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data: Dict[str, Any]) -> Task:
        request = self.context["request"]
        try:
            return task_providers.create_task_by_data(
                created_by_id=request.user.id,
                company_id=request.user.company_id,
                project_uuid=validated_data["project_uuid"],
                assigned_to_id=validated_data["assigned_to"],
                title=validated_data["title"],
                content=validated_data["content"],
                due_date=validated_data["due_data"],
            )
        except IntegrityError as ex:
            raise ValidationError({"IntegrityError": str(ex)})


class ProjectSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, allow_null=True)
    company_id = serializers.IntegerField()
    name = serializers.CharField()
    members = MembersField(required=False, allow_null=True)
    kind = serializers.IntegerField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data: Dict[str, Any]) -> Project:
        request = self.context["request"]
        validated_data.pop("company_id")

        project = project_providers.create_project_by_company_and_user_id(
            user_id=request.user.id,
            company_id=request.user.company_id,
            **validated_data,
        )

        return project
