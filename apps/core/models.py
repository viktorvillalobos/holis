from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import ImageField, get_thumbnail

# Create your models here.


class Company(TimeStampedModel):
    """
        Tenant model
    """

    name = models.CharField(_("name"), max_length=50, db_index=True)
    code = models.CharField(_("code"), max_length=50, db_index=True, unique=True)
    email = models.EmailField(_("email"), null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)
    logo = ImageField(_("logo"), blank=True, null=True, upload_to="logo")

    tenant_id = "id"

    class Meta:
        ordering = ["name"]
        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self):
        return self.name

    @property
    def logo_thumb(self):
        if not self.logo:
            return None
        return get_thumbnail(self.logo.file, "100x100", crop="center", quality=99).url


class Area(MPTTModel):
    """
        Company distribution unit, allow to organize a
        company.

        example:

        - Adslab North
          - Sales.
          - Marketing.
        - Adslab South
          - Development.
          - Operations.
    """

    company = models.ForeignKey(
        "core.Company",
        related_name="areas",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    width = models.PositiveIntegerField(_("Width"), default=30)
    height = models.PositiveIntegerField(_("Height"), default=30)
    state = JSONField(default=list, blank=True)

    tenant_id = "company_id"

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def users_online(self):
        # from apps.core.uc import area_uc

        # uc = area_uc.GetStateAreaUC(self)
        # return len(uc.connected_idxs)
        return len(self.state)


class Announcement(TimeStampedModel):
    company = models.ForeignKey(
        "core.Company",
        related_name="announcements",
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )

    title = models.CharField(_("title"), max_length=100, blank=True)
    text = models.TextField(_("text"), blank=True)

    created_by = models.ForeignKey(
        "users.User", related_name="announcements", on_delete=models.CASCADE
    )

    tenant_id = "company_id"

    class Meta:
        ordering = ["-created"]
        unique_together = ["id", "company"]


class ChangeLog(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=50)
    text = models.TextField(_("text"), blank=True)

    created_by = models.ForeignKey(
        "users.User", related_name="changelogs", on_delete=models.CASCADE
    )

    tenant_id = "company_id"

    class Meta:
        ordering = ["-created"]
