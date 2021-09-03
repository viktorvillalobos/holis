# Generated by Django 3.2 on 2021-09-03 22:59

from django.db import migrations

import uuid


def gen_uuid(apps, schema_editor):
    User = apps.get_model("users", "User")
    for row in User.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_user_uuid"),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop)
    ]
