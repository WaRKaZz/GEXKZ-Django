# Generated by Django 3.0.5 on 2020-04-07 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200407_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='telegramm',
            new_name='telegram',
        ),
    ]