# Generated by Django 4.2.16 on 2024-10-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_listing_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='000-0000-0000', max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='geolocation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]