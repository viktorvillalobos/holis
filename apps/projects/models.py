from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _

import uuid
from model_utils.models import SoftDeletableModel, TimeStampedModel


class BaseModel(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ProjectBaseModel(BaseModel, SoftDeletableModel):
    class Meta:
        abstract = True


class Project(ProjectBaseModel):
    """
    Management struct is an abstract model that defines the way
    how we handle data for the following structures:

    * Teams.
    * Projects.
    * Company

    """

    COMPANY = 1
    TEAM = 2
    PROJECT = 3

    PROJECT_KIND_CHOICES = ((COMPANY, "Company"), (TEAM, "Team"), (PROJECT, "Project"))

    company = models.ForeignKey(
        "core.Company",
        related_name="all_projects",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    name = models.CharField(max_length=100)
    members = models.ManyToManyField("users.User")
    kind = models.IntegerField(choices=PROJECT_KIND_CHOICES, db_index=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["company_id"],
                condition=Q(kind=1),
                name="unique_company_id_kind_idx",
            )
        ]


class BoardMessage(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_board_messages",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )

    project = models.ForeignKey(
        Project, related_name="board_messages", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="board_message"
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]


class BoardMessageComment(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_board_message_comments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    project = models.ForeignKey(
        Project, related_name="board_message_comments", on_delete=models.CASCADE
    )

    instance = models.ForeignKey(
        BoardMessage, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="board_message_comments"
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]


class Task(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_tasks",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )

    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)

    assigned_to = models.ForeignKey(
        "users.User", related_name="tasks", on_delete=models.DO_NOTHING
    )
    due_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["uuid", "company"]


class TaskComment(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_tasks_comments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    instance = models.ForeignKey(
        Task, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="task_comments"
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]


class Attachment(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_attachments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    project = models.ForeignKey(
        Project, related_name="attachments", on_delete=models.CASCADE
    )
    file = models.FileField()
    mime = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ["uuid", "company"]


class AttachmentComment(ProjectBaseModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="all_attachments_comments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    instance = models.ForeignKey(
        Attachment, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="attachment_comments"
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]
