# Generated by Django 3.1.7 on 2021-04-23 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20210422_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]