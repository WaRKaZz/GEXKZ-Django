from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse


class Platform(models.Model):
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40, null=True)
    rawg_id = models.PositiveIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name + ' rawg_id=' + str(self.rawg_id)


class Genre(models.Model):
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40, null=True)
    rawg_id = models.PositiveIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name + ' rawg_id=' + str(self.rawg_id)


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(default='default-game-image.jpg',
                              upload_to='game_pics')
    genre = models.ManyToManyField(Genre)
    likes = models.PositiveIntegerField(default=0)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.platform.name

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        width, height = image.size
        proportion = width / height
        if proportion > 1.778:
            new_height = 563
            new_width = int(new_height * width / height)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            x1, y1, x2, y2 = int(new_width / 2) - \
                500, 0, int(new_width / 2) + 500, 563
            image = image.crop((x1, y1, x2, y2))
            image.save(self.image.path)
        elif proportion < 1.776:
            new_width = 1000
            new_height = int(new_width * height / width)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            x1, y1, x2, y2 = 0, int(new_height / 2) - \
                281, 1000, int(new_height / 2) + 281
            image = image.crop((x1, y1, x2, y2))
            image.save(self.image.path)
        elif height > 1000 or width > 1000:
            output_size = (1000, 1000)
            image.thumbnail(output_size)
            image.save(self.image.path)

    def get_absolute_url(self):
        return reverse('gex-game-datail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class Comment(models.Model):
    message = models.CharField(max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comment_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_comment_set',
                             blank=True,
                             null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    liked_by = models.ManyToManyField(
        User, related_name='user_liked_comment_set')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-likes', '-date_posted']


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
