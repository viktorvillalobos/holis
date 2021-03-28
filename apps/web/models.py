from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from model_utils.models import TimeStampedModel

from apps.utils.fields import LowerCharField

# Create your models here.


class Lead(TimeStampedModel):
    """
        A lead is a user who init the process but is incomplete
    """

    email = models.EmailField(_("Email"))
    password = models.CharField(_("Password"), max_length=255, blank=True, null=True)
    company_name = models.CharField(
        _("Company name"), blank=True, null=True, max_length=100
    )
    company_code = LowerCharField(
        _("Company code"), blank=True, null=True, max_length=20, db_index=True
    )
    name = models.CharField(_("User name"), blank=True, null=True, max_length=100)
    position = models.CharField(_("Position"), max_length=50, blank=True, null=True)
    avatar = models.ImageField(_("Avatar"), blank=True, null=True)
    secret = models.UUIDField(_("secret"), default=uuid.uuid4, editable=False)
    invitations = ArrayField(models.EmailField(_("Email")), default=list)

    def __str__(self):
        return self.email
