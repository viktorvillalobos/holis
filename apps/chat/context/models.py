from typing import Optional

from django.contrib.postgres.indexes import GinIndex
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import uuid
from model_utils.models import TimeStampedModel

from apps.utils.fields import UUIDForeignKey

"""
Design Concepts
========

1. All is a room.

"""


class Room(TimeStampedModel):
    """
    Chat Room
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company",
        related_name="channels",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
        db_index=True,
    )
    name = models.CharField(_("title"), db_index=True, max_length=255)
    subject = models.CharField(_("subject"), max_length=1024, null=True, blank=True)
    members = models.ManyToManyField(
        "users.User", related_name="members", verbose_name=_("members")
    )
    owners = models.ManyToManyField(
        "users.User", related_name="owners", verbose_name=_("owners"), blank=True
    )
    admins = models.ManyToManyField(
        "users.User", related_name="admins", verbose_name=_("admins"), blank=True
    )
    outcasts = models.ManyToManyField(
        "users.User", related_name="outcats", verbose_name=_("outcats"), blank=True
    )
    max_users = models.IntegerField(_("Max users"), default=0)
    password = models.CharField(_("password"), max_length=255, null=True, blank=True)
    service_name = models.CharField(
        _("Service Name"), max_length=255, default="conference"
    )

    is_public = models.BooleanField(_("is public"), default=True)
    persistent = models.BooleanField(_("is persistent"), default=True)
    any_can_invite = models.BooleanField(_("Any can invite"), default=True)
    members_only = models.BooleanField(_("members only"), default=False)
    is_conversation = models.BooleanField(
        _("is conversation"), default=False, db_index=True
    )
    is_one_to_one = models.BooleanField(
        _("is one to one"), default=False, db_index=True
    )
    image = models.ImageField(null=True, blank=True)

    # Last message info
    last_message_ts = models.DateTimeField(default=timezone.now, db_index=True)
    last_message_text = models.TextField(null=True, blank=True)
    last_message_user_id = models.IntegerField(null=True, blank=True)

    tenant_id = "company_id"

    class Meta:
        ordering = ["created"]
        unique_together = ["name", "company"]

    def __str__(self):
        return self.name

    @property
    def image_url(self) -> Optional[str]:
        return self.image.url if self.image else None


class Message(TimeStampedModel):
    """
    A message from an user
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_uuid = models.UUIDField(null=True)
    company = models.ForeignKey(
        "core.Company",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
        db_index=True,
    )
    room = UUIDForeignKey(
        Room,
        verbose_name=_("room"),
        related_name="messages",
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField(_("text"))
    reads = models.JSONField(
        _("reads"),
        db_index=True,
        default=dict,
        help_text="include a dict with user_id:timestamp",
    )

    tenant_id = "company_id"

    class Meta:
        indexes = [GinIndex(fields=["reads"])]
        unique_together = ["uuid", "company"]


class RoomUserRead(models.Model):
    """
    Contains the last time read timestamp by user
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="room_user_reads",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = UUIDForeignKey(
        Room,
        verbose_name=_("room"),
        related_name="room_user_reads",
        on_delete=models.CASCADE,
        db_index=True,
        db_constraint=False,
    )
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ["company", "user", "room"]


def chat_attachments_path(instance, file_name):
    return f"{instance.company_id}/chat/room/{instance.message.room_uuid}/attachments/{file_name}"


class MessageAttachment(TimeStampedModel):
    """
    Message Attachment
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company",
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    message = UUIDForeignKey(
        Message,
        verbose_name=_("message"),
        related_name="attachments",
        on_delete=models.CASCADE,
    )
    attachment = models.FileField(_("attachment"), upload_to=chat_attachments_path)
    mimetype = models.CharField(_("Mimetype"), blank=True, null=True, max_length=255)

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]
        ordering = ["created"]
        verbose_name = _("message attachment")
        verbose_name_plural = _("message attachments")
