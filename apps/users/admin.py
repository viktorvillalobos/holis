from apps.users import models
from apps.users.forms import UserChangeForm, UserCreationForm
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from sorl.thumbnail.admin import AdminImageMixin

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "company",
            "jid",
        )


@admin.register(User)
class UserAdmin(AdminImageMixin, auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    add_fieldsets = (
        (
            "Basic",
            {
                "classes": ("wide",),
                "fields": ("company", "username", "password1", "password2"),
            },
        ),
        (
            "Profile",
            {
                "classes": ("wide",),
                "fields": ("jid", "name"),
            },
        ),
    )

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "company",
                    "name",
                    "position",
                    "avatar",
                    "birthday",
                    "default_area",
                    "jid",
                )
            },
        ),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = [
        "username",
        "company",
        "name",
        "is_superuser",
    ]
    search_fields = ["name"]
    filter_fields = ["company"]


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["text", "user", "is_active"]


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["company", "user", "title", "unread", "created"]
