# Generated by Django 3.2 on 2021-05-26 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_auto_20210526_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish')], default='en', max_length=2),
        ),
    ]