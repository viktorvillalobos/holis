from apps.core import models
from django.contrib import admin


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass
