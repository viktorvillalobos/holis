# Generated by Django 3.0.5 on 2020-07-26 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_status_icon_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Seen'),
        ),
    ]