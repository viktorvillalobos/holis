from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


"""
Design Concepts
========

1. All is a channel.


"""


class Channel(TimeStampedModel):
    """
        Channel represent a instnace of a group of communication
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="channels",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
        db_index=True,
    )
    users = models.ManyToManyField(
        "users.User", related_name="channels", verbose_name=_("users"),
    )
    name = models.CharField(
        _("title"), db_index=True, primary_key="name", max_length=255
    )
    is_public = models.BooleanField(_("is public"), default=True)

    tenant_id = "company_id"

    class Meta:
        ordering = ["-created"]
        unique_together = ["name", "company"]

    def __str__(self):
        return self.title


class Message(TimeStampedModel):
    """
        A message from an user
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    channel = models.ForeignKey(
        Channel,
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
        ordering = ["-created"]


class MessageAttachment(TimeStampedModel):
    """
        Message Attachment
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    message = models.ForeignKey(
        Message,
        verbose_name=_("message"),
        related_name="messages",
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
