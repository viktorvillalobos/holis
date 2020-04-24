from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("name of user"), blank=True, max_length=255)
    company = models.ForeignKey(
        "core.Company",
        verbose_name=_("company"),
        on_delete=models.CASCADE,
        related_name="users",
    )
    position = models.CharField(_("position"), blank=True, null=True, max_length=100)

    tenant_id = "company_id"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        ordering = ["-id"]
        unique_together = ["id", "company"]


class Status(TimeStampedModel):
    """
        Single Status
    """

    company = models.ForeignKey(
        "core.Company",
        verbose_name=_("company"),
        on_delete=models.CASCADE,
        related_name="statuses",
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="statuses",
        on_delete=models.CASCADE,
    )
    text = models.CharField(_("name"), max_length=100)
    icon = models.ImageField(_("icon"), null=True, blank=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    tenant_id = ["company_id"]

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["-pk"]
        verbose_name = _("status")
        verbose_name_plural = _("statuses")

    def __str__(self):
        return self.text


class UserNotification(TimeStampedModel):
    """
        User notification
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="notifications",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unread = models.BooleanField(
        _("unread"), default=True, blank=False, db_index=True
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["-created"]
        verbose_name = _("user notification")
        verbose_name_plural = _("user notifications")
