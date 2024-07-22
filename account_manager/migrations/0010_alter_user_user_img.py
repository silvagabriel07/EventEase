# Generated by Django 5.0.7 on 2024-07-21 04:19

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_manager', '0009_alter_user_idade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_img',
            field=django_resized.forms.ResizedImageField(crop=None, default='/user_img/user_img.png', force_format=None, keep_meta=True, quality=85, scale=None, size=[600, 600], upload_to='user_img'),
        ),
    ]