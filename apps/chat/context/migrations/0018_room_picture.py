# Generated by Django 3.2 on 2021-08-16 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_message_app_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
