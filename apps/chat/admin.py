from django.contrib import admin

from apps.chat import models

# Register your models here.


@admin.register(models.Channel)
class ChatModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Message)
class MessageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MessageAttachment)
class MessageAttachmentModelAdmin(admin.ModelAdmin):
    pass
