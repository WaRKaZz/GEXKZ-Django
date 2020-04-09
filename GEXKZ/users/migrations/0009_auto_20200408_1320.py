# Generated by Django 3.0.5 on 2020-04-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200407_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ban_commentary',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='rules',
            field=models.CharField(choices=[('M', 'Moderator'), ('U', 'User')], default='U', max_length=1),
        ),
    ]