# Generated by Django 3.0.5 on 2020-04-18 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameexch', '0005_auto_20200409_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamecomment',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='usercomment',
            name='likes',
        ),
    ]
