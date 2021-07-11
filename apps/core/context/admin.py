from django.contrib import admin

from . import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "code", "email")
    list_filter = ["country"]
    search_fields = ["name"]


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "users_online", "parent", "company", "width", "height")
    list_filter = ["company"]
    search_fields = ["name"]


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created", "modified")
    list_filter = ["company"]
    search_fields = ["title"]


@admin.register(models.ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created", "modified")
    search_fields = ["title"]
