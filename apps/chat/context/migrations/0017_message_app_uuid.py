# Generated by Django 3.2 on 2021-08-07 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20210702_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='app_uuid',
            field=models.UUIDField(null=True),
        ),
    ]