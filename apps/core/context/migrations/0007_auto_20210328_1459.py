# Generated by Django 3.1.7 on 2021-03-28 14:59

from django.db import migrations

import apps.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210131_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='code',
            field=apps.utils.fields.LowerCharField(db_index=True, max_length=50, unique=True, verbose_name='code'),
        ),
    ]