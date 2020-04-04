from django.shortcuts import render
from .models import Game

def home(request):
	context = {
		'games': Game.objects.all()
	}
	return render(request, 'gameexch/home.html', context)

def about(request):
	return render(request, 'gameexch/about.html', {'title':'About'})
