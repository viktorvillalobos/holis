# Generated by Django 3.1.7 on 2021-04-05 03:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20210405_0321'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageContentTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('lang', models.CharField(choices=[('es', 'Spanish')], db_index=True, max_length=2)),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.page')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
