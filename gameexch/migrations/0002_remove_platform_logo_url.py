# Generated by Django 3.0.7 on 2020-11-07 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameexch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='logo_url',
        ),
    ]
