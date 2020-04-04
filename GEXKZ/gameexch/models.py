from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


USER_RULES = (
	('A', 'Admin'),
	('T', 'Technichian'),
	('M', 'Moderator'),
	('U', 'User'),
	)


class Console(models.Model):
	name = models.CharField(max_length=40)
	logo_url = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name


class City(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name


class Game(models.Model):
	name = models.CharField(max_length=40)
	description = models.TextField()
	image_url = models.CharField(max_length=100)
	genre = models.CharField(max_length=30)
	likes = models.PositiveIntegerField()
	console = models.ForeignKey(Console, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name + " " + self.console.name


class UserComment(models.Model):
	message = models.TextField()
	number = models.PositiveIntegerField()
	likes = models.PositiveIntegerField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE,
							   related_name='author_comment_set')
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							 related_name='user_comment_set')
	
	def __str__(self):
		return self.message

class GameComment(models.Model):
	message = models.TextField()	
	number = models.PositiveIntegerField()
	likes = models.PositiveIntegerField()
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
	is_wanted = models.BooleanField(default=0)
	is_owner = models.BooleanField(default=0)
	is_like = models.BooleanField(default=0)
	price = models.PositiveIntegerField()
	currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,
								null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.id
	
