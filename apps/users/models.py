import datetime as dt
import requests
from sorl.thumbnail import ImageField
from birthday.fields import BirthdayField
from birthday.managers import BirthdayManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from sorl.thumbnail import get_thumbnail


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
    position = models.CharField(
        _("position"), blank=True, null=True, max_length=100
    )
    default_area = models.ForeignKey(
        "core.Area", blank=True, null=True, on_delete=models.SET_NULL,
    )
    birthday = BirthdayField()

    avatar = ImageField(
        _("avatar"), blank=True, null=True, upload_to="avatars"
    )

    objects = UserManager()

    tenant_id = "company_id"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        ordering = ["-id"]
        unique_together = ["id", "company"]

    @property
    def current_status(self):
        return self.statuses.filter(is_active=True).first()

    def save(self, *args, **kwargs):
        # if not self.avatar:
        #     self.avatar = self.get_monster()
        super().save(*args, **kwargs)

    def get_monster(self):
        pass

    @property
    def avatar_thumb(self):
        if not self.avatar:
            return f"https://api.adorable.io/avatars/100/{self.username}@adorable.png"

        return get_thumbnail(
            self.avatar.file, '100x100', crop='center', quality=99
        ).url


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

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["-pk"]
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
    unread = models.BooleanField(
        _("unread"), default=True, blank=False, db_index=True
    )

    tenant_id = "company_id"

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["-created"]
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
