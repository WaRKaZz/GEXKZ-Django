# Generated by Django 3.0.7 on 2020-11-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameexch', '0002_remove_platform_logo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='ravg_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
