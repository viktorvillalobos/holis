# Generated by Django 3.0.5 on 2020-07-26 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_create_default_company'),
        ('users', '0003_user_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currents', to='core.Area'),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='defaults', to='core.Area'),
        ),
    ]