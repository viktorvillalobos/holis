from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations

import datetime as dt
import uuid

NOT_CREATE_DEFAULT_DATA = settings.ENVIRONMENT is settings.TESTING


def create_base_status(StatusModel, user):
    if NOT_CREATE_DEFAULT_DATA:
        return

    base = [
        {
            "company": user.company,
            "user": user,
            "icon": "💻",
            "text": "Available",
            "is_active": True,
        },
        {
            "company": user.company,
            "user": user,
            "icon": "🤝",
            "text": "Metting",
            "is_active": False,
        },
        {
            "company": user.company,
            "user": user,
            "icon": "😋",
            "text": "Having launch",
            "is_active": False,
        },
        {
            "company": user.company,
            "user": user,
            "icon": "👻",
            "text": "Absent",
            "is_active": False,
        },
    ]

    objects = [StatusModel(**x) for x in base]

    StatusModel.objects.bulk_create(objects)


def create_django_user(UserModel, company, email, name, position, birthday):
    if NOT_CREATE_DEFAULT_DATA:
        return

    return UserModel.objects.create(
        uuid=uuid.uuid4(),
        company=company,
        email=email,
        username=email,
        birthday=birthday,
        name=name,
        position=position,
        password=make_password("holis123"),
        is_superuser=True,
        is_staff=True,
    )


def create_base_users(apps, schema_editor):
    if NOT_CREATE_DEFAULT_DATA:
        return

    Company = apps.get_model("core", "Company")
    User = apps.get_model("users", "User")
    Status = apps.get_model("users", "Status")
    adslab = Company.objects.get(code="adslab")
    firesoft = Company.objects.get(code="firesoft")

    user1 = create_django_user(
        User,
        adslab,
        "viktor@hol.is",
        "Viktor",
        "CTO",
        dt.date(1992, 4, 14),
    )
    user2 = create_django_user(
        User,
        adslab,
        "julls@hol.is",
        "Julls",
        "Product Maker",
        dt.date(1995, 8, 15),
    )
    user3 = create_django_user(
        User,
        firesoft,
        "viktor@firesoft.org",
        "Viktor",
        "CTO",
        dt.date(1992, 4, 14),
    )
    user4 = create_django_user(
        User,
        firesoft,
        "julls@firesoft.org",
        "Julls",
        "Product Maker",
        dt.date(1995, 8, 15),
    )

    create_base_status(Status, user1)
    create_base_status(Status, user2)
    create_base_status(Status, user3)
    create_base_status(Status, user4)


def reverse_base_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    Status = apps.get_model("users", "Status")
    User.objects.all().delete()
    Status.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("users", "0012_remove_user_uuid_null")]

    operations = [migrations.RunPython(create_base_users, reverse_base_users)]
