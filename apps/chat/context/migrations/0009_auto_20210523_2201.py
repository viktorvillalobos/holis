# Generated by Django 3.2 on 2021-05-23 22:01

import django.db.models.deletion
from django.db import migrations

import apps.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0008_auto_20210523_2129"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="room",
            field=apps.utils.fields.UUIDForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="chat.room",
                verbose_name="room",
            ),
        ),
        migrations.AlterField(
            model_name="messageattachment",
            name="message",
            field=apps.utils.fields.UUIDForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attachments",
                to="chat.message",
                verbose_name="message",
            ),
        ),
    ]
