# Generated by Django 3.0.7 on 2020-11-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameexch', '0012_auto_20201109_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.CharField(max_length=250),
        ),
    ]