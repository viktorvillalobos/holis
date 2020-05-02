from apps.users import models
from apps.users.forms import UserChangeForm, UserCreationForm
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from sorl.thumbnail.admin import AdminImageMixin

User = get_user_model()


@admin.register(User)
class UserAdmin(AdminImageMixin, auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {"fields": ("name", "avatar")}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["company", "username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "is_active"]


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["company", "user", "title", "unread", "created"]
