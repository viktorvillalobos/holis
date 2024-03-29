from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from apps.web.models import BlogCategory, BlogEntry, Lead, Page

# Register your models here.


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "company_name",
        "company_code",
        "name",
        "created",
        "modified",
    )
    search_fields = ("email", "company")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": AdminMartorWidget}}
    list_display = ("title", "slug", "created", "modified")
    search_fields = ("title", "is_draft")


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created", "modified")
    search_fields = ("name",)


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": AdminMartorWidget}}
    list_display = ("title", "lang", "category", "slug", "created", "modified")
    search_fields = ("title", "is_draft")
