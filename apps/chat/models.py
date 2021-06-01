from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
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
        "users.User", related_name="owners", verbose_name=_("owners")
    )
    admins = models.ManyToManyField(
        "users.User", related_name="admins", verbose_name=_("admins")
    )
    outcasts = models.ManyToManyField(
        "users.User", related_name="outcats", verbose_name=_("outcats")
    )
    max_users = models.IntegerField(_("Max users"), default=0)
    password = models.CharField(_("password"), max_length=255, null=True, blank=True)
    service_name = models.CharField(
        _("Service Name"), max_length=255, default="conference"
    )

    is_public = models.BooleanField(_("is public"), default=True)
    persistent = models.BooleanField(_("is public"), default=True)
    any_can_invite = models.BooleanField(_("Any can invite"), default=True)
    members_only = models.BooleanField(_("members only"), default=False)
    is_one_to_one = models.BooleanField(_("is one to one"), default=False)

    tenant_id = "company_id"

    class Meta:
        ordering = ["created"]
        unique_together = ["name", "company"]

    def __str__(self):
        return self.name


class Message(TimeStampedModel):
    """
    A message from an user
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        "core.Company",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )

    room = UUIDForeignKey(
        Room, verbose_name=_("room"), related_name="messages", on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="messages",
    )

    text = models.TextField(_("text"))

    created = CreationDateTimeField(_("created"), db_index=True)
    modified = ModificationDateTimeField(_("modified"))

    tenant_id = "company_id"

    class Meta:
        unique_together = ["uuid", "company"]
        ordering = ["-created"]


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


class RoomRead(TimeStampedModel):
    """
    Record of the last time an user check a group, this is used
    to take control about the unread messages
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    company = models.ForeignKey(
        "core.Company",
        related_name="room_reads",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )

    room = UUIDForeignKey(
        Room, verbose_name=_("room"), related_name="reads", on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "users.User", related_name="room_reads", on_delete=models.DO_NOTHING
    )

    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ["uuid", "company", "room", "user"]
        verbose_name = _("room read")
        verbose_name_plural = _("room reads")
