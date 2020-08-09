import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


"""
Design Concepts
========

1. All is a room.

"""


class Room(TimeStampedModel):
    """
        Chat Room
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company",
        related_name="channels",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
        db_index=True,
    )
    name = models.CharField(_("title"), db_index=True, max_length=255)
    subject = models.CharField(
        _("subject"), max_length=1024, null=True, blank=True
    )
    members = models.ManyToManyField(
        "users.User", related_name="members", verbose_name=_("members"),
    )
    owners = models.ManyToManyField(
        "users.User", related_name="owners", verbose_name=_("owners"),
    )
    admins = models.ManyToManyField(
        "users.User", related_name="admins", verbose_name=_("admins"),
    )
    outcasts = models.ManyToManyField(
        "users.User", related_name="outcats", verbose_name=_("outcats"),
    )
    max_users = models.IntegerField(_("Max users"), default=0)
    password = models.CharField(
        _("password"), max_length=255, null=True, blank=True
    )
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    room = models.ForeignKey(
        Room,
        verbose_name=_("channel"),
        related_name="messages",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField(_("text"))

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["created"]


class MessageAttachment(TimeStampedModel):
    """
        Message Attachment
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company",
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    message = models.ForeignKey(
        Message,
        verbose_name=_("message"),
        related_name="attachments",
        on_delete=models.CASCADE,
    )
    attachment = models.FileField(_("attachment"))
    mimetype = models.CharField(
        _("Mimetype"), blank=True, null=True, max_length=255
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["created"]
        verbose_name = _("message attachment")
        verbose_name_plural = _("message attachments")

    def __str__(self):
        return self.attachment.file.url
