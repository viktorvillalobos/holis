# Generated by Django 3.2 on 2021-07-02 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_room_last_message_ts'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_message_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='last_message_user_id',
            field=models.IntegerField(null=True),
        ),
    ]