from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Console(models.Model):
    name = models.CharField(max_length=40)
    short_name = models.CharField(max_length=5, null=True)
    logo_url = models.ImageField(default='default-console-logo.jpg',
                                 upload_to='console_pics')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    image = models.ImageField(default='default-game-image.jpg',
                              upload_to='game_pics')
    genre = models.CharField(max_length=30)
    likes = models.PositiveIntegerField(default=0)
    console = models.ForeignKey(Console, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.console.name

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('gex-game-datail', kwargs={'pk': self.pk})


class UserComment(models.Model):
    message = models.TextField(max_length=240)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comment_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_comment_set')

    def __str__(self):
        return self.message


class GameComment(models.Model):
    message = models.TextField(max_length=240)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Currency(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class UserToGame(models.Model):
    is_wanted = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    price = models.PositiveIntegerField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        string = ''
        if self.is_wanted:
            string = f'{self.user.username} wants {self.game.name}'
        elif self.is_owner:
            string = f'{self.user.username} owns {self.game.name}'
        elif self.is_like:
            string += f'{self.user.username} likes {self.game.name}'
        else:
            string = 'Some strange'
        return string
