# Generated by Django 5.0.7 on 2024-07-21 23:45

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0013_alter_event_event_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_banner',
            field=django_resized.forms.ResizedImageField(crop=None, default='event_banners/default_event_banner.png', force_format=None, keep_meta=True, quality=85, scale=None, size=[600, 600], upload_to='event_banners'),
        ),
    ]