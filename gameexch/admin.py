from django.contrib import admin
from .models import *

admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(City)
admin.site.register(Game)
admin.site.register(Comment)
admin.site.register(Currency)
admin.site.register(UserToGame)
