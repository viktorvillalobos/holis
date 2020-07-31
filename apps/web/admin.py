from django.contrib import admin

from apps.web.models import Lead

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
