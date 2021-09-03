# Generated by Django 3.2 on 2021-09-03 22:58

from django.db import migrations, models

import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_userinvitation"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
