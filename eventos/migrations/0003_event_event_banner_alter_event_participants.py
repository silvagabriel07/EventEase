# Generated by Django 4.2.3 on 2023-07-13 02:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventos', '0002_alter_event_free_alter_event_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_banner',
            field=models.ImageField(default='event_banners/default_event_banner.png', upload_to='media'),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='event_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]