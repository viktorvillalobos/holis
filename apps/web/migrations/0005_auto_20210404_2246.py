# Generated by Django 3.1.7 on 2021-04-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]