# Generated by Django 3.0.5 on 2020-05-02 21:11

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='avatar'),
        ),
    ]