from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid
from django_extensions.db.fields import AutoSlugField
from model_utils.models import TimeStampedModel
from slugify import slugify
from taggit.managers import TaggableManager

from apps.utils.fields import LowerCharField

from .lib import constants as web_constants

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


class Page(TimeStampedModel):
    """
    A custom page
    """

    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True, db_index=True)
    slug = AutoSlugField(
        populate_from="title", slugify_function=slugify, max_length=255
    )
    image = models.ImageField(upload_to="holis/pages/", null=True, blank=True)


class PageContentTranslation(TimeStampedModel):
    ES = "es"
    LANG_CHOICES = ((ES, "Spanish"),)

    page = models.ForeignKey("web.Page", on_delete=models.CASCADE)
    lang = models.CharField(db_index=True, max_length=2, choices=LANG_CHOICES)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", slugify_function=slugify, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"


class BlogEntry(TimeStampedModel):
    """
    A custom page
    """

    category = models.ForeignKey(
        "web.BlogCategory", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True, db_index=True)
    slug = AutoSlugField(
        populate_from="title", slugify_function=slugify, max_length=255
    )
    image = models.ImageField(upload_to="holis/blog/", null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = "Blog Entries"
        verbose_name_plural = "Blog Entries"

    def __str__(self):
        return self.title


class BlogEntryContentTranslation(TimeStampedModel):
    ES = "es"
    LANG_CHOICES = web_constants.BlogEntryLangChoices.choices

    blog_entry = models.ForeignKey("web.BlogEntry", on_delete=models.CASCADE)
    lang = models.CharField(db_index=True, max_length=2, choices=LANG_CHOICES)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
