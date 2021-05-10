# Generated by Django 3.1.7 on 2021-04-10 03:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import django_extensions.db.fields
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_pagecontenttranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True)),
                ('is_draft', models.BooleanField(db_index=True, default=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from='title')),
                ('image', models.ImageField(blank=True, null=True, upload_to='holis/blog/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='holis/pages/'),
        ),
        migrations.CreateModel(
            name='BlogEntryContentTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('lang', models.CharField(choices=[('es', 'Spanish')], db_index=True, max_length=2)),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True)),
                ('blog_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.blogentry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]