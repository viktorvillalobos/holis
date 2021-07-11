# Generated by Django 3.2 on 2021-06-28 16:27

from django.conf import settings
from django.db import migrations

from model_bakery import baker


def create_demo_users(apps, schema_editor):
    Company = apps.get_model("core", "Company")
    company = Company.objects.get(code="adslab")

    if not settings.ENVIRONMENT == settings.TESTING:
        baker.make("users.User", company_id=company.id, _quantity=10)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_user_last_seen"),
    ]

    operations = [migrations.RunPython(create_demo_users)]
