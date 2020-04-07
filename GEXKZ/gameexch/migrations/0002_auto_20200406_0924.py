# Generated by Django 3.0.5 on 2020-04-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameexch', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='image_url',
        ),
        migrations.AddField(
            model_name='console',
            name='short_name',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='image',
            field=models.ImageField(default='default-game-image.jpg', upload_to='game_pics'),
        ),
        migrations.AlterField(
            model_name='console',
            name='logo_url',
            field=models.ImageField(default='default-console-logo.jpg', upload_to='console_pics'),
        ),
    ]