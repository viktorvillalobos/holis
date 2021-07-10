# Generated by Django 3.2 on 2021-06-10 01:35

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("context", "0010_message_reads"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="reads",
            field=models.JSONField(
                db_index=True,
                default=dict,
                help_text="include a dict with user_id:timestamp",
                verbose_name="reads",
            ),
        ),
        migrations.AddIndex(
            model_name="message",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["reads"], name="chat_messag_reads_a775f8_gin"
            ),
        ),
    ]