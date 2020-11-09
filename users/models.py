from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from gameexch.models import City, Game
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

RULES = (("A", "Administrator"), ("M", "Moderator"), ("U", "User"))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default-profile-image.jpg", upload_to="profile_pics", blank=True
    )
    vk = models.CharField(max_length=200, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    whatsapp = PhoneNumberField(null=True, blank=True)
    telegram = PhoneNumberField(null=True, blank=True)
    ban_commentary = models.TextField(null=True)
    rules = models.CharField(choices=RULES, max_length=1, default="U")
    banned = models.BooleanField(default=False)
    likes = models.ManyToManyField(Game, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("profile-view", kwargs={"pk": self.pk})
