# Generated by Django 4.2.3 on 2023-07-13 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_alter_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_banner',
            field=models.FileField(default='event_banners/default_event_banner.png', upload_to='event_banners'),
        ),
    ]
