from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import files
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

import datetime as dt
import logging
import requests
from birthday.fields import BirthdayField
from birthday.managers import BirthdayManager
from io import BytesIO
from model_utils.models import TimeStampedModel
from sorl.thumbnail import ImageField  # , get_thumbnail

from apps.core.context.models import Area

logger = logging.getLogger(__name__)


class UserManager(BirthdayManager, UserManager):
    def create_superuser(self, username, email, password, company) -> "User":
        if password is None:
            raise TypeError("Superusers must have a password.")

        birthday = dt.datetime.now().date()

        data = {
            "username": username,
            "email": email,
            "password": password,
            "company": company,
            "birthday": birthday,
            "is_superuser": True,
            "is_staff": True,
        }

        return self.create_user(**data)


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
    default_area = models.ForeignKey(
        "core.Area",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="defaults",
    )
    current_area = models.ForeignKey(
        "core.Area",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="currents",
        db_index=True,
    )
    birthday = BirthdayField(null=True, blank=True)

    avatar = ImageField(_("avatar"), blank=True, null=True, upload_to="avatars")
    jid = models.CharField(
        _("Jabber ID"), blank=True, null=True, max_length=100, db_index=True
    )
    last_seen = models.DateTimeField(
        _("Last Seen"), null=True, blank=True, db_index=True
    )

    objects = UserManager()

    tenant_id = "company_id"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        unique_together = ["id", "company"]

    @cached_property
    def avatar_thumb(self):
        if settings.ENVIRONMENT is not settings.TESTING:
            if not self.avatar:
                url = f"https://ui-avatars.com/api/?name={self.username}&background=random"
                resp = requests.get(url)
                fp = BytesIO()
                fp.write(resp.content)
                file_name = self.username + ".png"
                self.avatar.save(file_name, files.File(fp))
                self.save()

        # return get_thumbnail(self.avatar.file, "100x100", crop="center", quality=99).url

        return self.avatar.url if self.avatar else None

    def __str__(self):
        return f"{self.id} -> {self.name}"


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
        User, verbose_name=_("user"), related_name="statuses", on_delete=models.CASCADE
    )
    text = models.CharField(_("name"), max_length=100)
    icon_text = models.CharField(_("icon text"), max_length=20, blank=True)
    icon = models.ImageField(_("icon"), null=True, blank=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        verbose_name = _("status")
        verbose_name_plural = _("statuses")

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.pk is None:
            Status.objects.filter(user=self.user).update(is_active=False)

        super().save(*args, **kwargs)


class Notification(TimeStampedModel):
    """
    User notification
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="notifications",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unread = models.BooleanField(_("unread"), default=True, blank=False, db_index=True)

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["-created"]
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
