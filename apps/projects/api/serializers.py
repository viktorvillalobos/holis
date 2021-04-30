from typing import Any, Dict, Union

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
    company_id = serializers.IntegerField(required=False, allow_null=True)
    uuid = serializers.UUIDField(required=False, allow_null=True)
    project_uuid = serializers.UUIDField(required=False, allow_null=True)
    assigned_to = UserField(required=False, allow_null=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    title = serializers.CharField()
    content = serializers.CharField()
    is_done = serializers.BooleanField(required=False, default=False)

    def __init__(self, *args, **kwargs):
        self.many = kwargs.pop("many", False)
        return super().__init__(many=self.many, *args, **kwargs)

    def create(self, validated_data: Dict[str, Any]) -> Union[Task, list[Task]]:
        project_uuid = self.context["project_uuid"]
        company_id = self.context["company_id"]
        user_id = self.context["user_id"]

        if self.many:
            task_list = [Task(**data) for data in validated_data]
            try:
                return task_providers.bulk_create_tasks_by_dataclasses(
                    to_create_tasks=task_list
                )
            except IntegrityError as ex:
                raise ValidationError({"IntegrityError": str(ex)})

        try:
            return task_providers.create_task_by_data(
                created_by_id=user_id,
                company_id=company_id,
                project_uuid=project_uuid,
                assigned_to_id=validated_data.get("assigned_to"),
                title=validated_data["title"],
                content=validated_data.get("content"),
                due_date=validated_data.get("due_date"),
            )
        except IntegrityError as ex:
            raise ValidationError({"IntegrityError": str(ex)})

    def update(
        self, instance: Task, validated_data: Dict[str, Any]
    ) -> Union[Task, list[Task]]:
        project_uuid = self.context["project_uuid"]
        company_id = self.context["company_id"]
        user_id = self.context["user_id"]

        try:
            result = task_providers.update_task_by_data(
                created_by_id=user_id,
                company_id=company_id,
                task_uuid=instance.uuid,
                project_uuid=project_uuid,
                assigned_to_id=validated_data.get("assigned_to"),
                title=validated_data["title"],
                content=validated_data.get("content"),
                due_date=validated_data.get("due_date"),
                is_done=validated_data.get("is_done", False),
            )

            return result
        except IntegrityError as ex:
            raise ValidationError({"IntegrityError": str(ex)})


class ProjectSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False, allow_null=True)
    company_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField()
    members = MembersField(required=False, allow_null=True)
    kind = serializers.IntegerField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

    def create(self, validated_data: Dict[str, Any]) -> Project:
        user_id = self.context["user_id"]
        company_id = self.context["company_id"]

        project = project_providers.create_project_by_company_and_user_id(
            user_id=user_id, company_id=company_id, **validated_data
        )

        return project
