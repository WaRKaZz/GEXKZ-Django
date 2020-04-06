from django.db import models
from django.contrib.auth.models import User
from gameexch.models import Console, City


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default-profile-image.jpg', 
						      upload_to='profile_pics')
	vk = models.CharField(max_length=200, null=True)
	consoles = models.ManyToManyField(Console)
	city = models.ForeignKey(City, on_delete=models.SET_NULL,
							 null=True)
	about = models.TextField(null=True)
	phone = models.CharField(max_length=200, null=True)
	has_whatsapp = models.BooleanField(default=False)
	has_telegramm = models.BooleanField(default=False)
	
	def __str__ (self):
		return f'{self.user.username} Profile'
	
	class Meta:
		ordering = ('user',)
