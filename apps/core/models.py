from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField

# Create your models here.


class Company(TimeStampedModel):
    """
        Tenant model
    """

    country = CountryField()
    name = models.CharField(_("name"), max_length=50, db_index=True)
    code = models.CharField(_("code"), max_length=50, db_index=True)
    email = models.EmailField(_("email"), null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)

    tenant_id = "id"

    class Meta:
        ordering = ["name"]
        verbose_name = _("company")
        verbose_name_plural = _("companies")


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
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    tenant_id = "company_id"

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ["id", "company"]
        ordering = ["name"]

    def __str__(self):
        return self.name
