# Generated by Django 3.0.5 on 2020-04-28 01:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200428_0104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='users',
        ),
        migrations.AddField(
            model_name='area',
            name='state',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
