from django.shortcuts import render
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView
)
from .models import Game

def home(request):
	context = {
		'games': Game.objects.all()
	}
	return render(request, 'gameexch/home.html', context)

def about(request):
	return render(request, 'gameexch/about.html', {'title':'About'})


class GameListView(ListView):
	model = Game 

class GameDetailView(DetailView):
	model = Game 

class GameCreateView(CreateView):
	model = Game
	fields['name', 'desctiption', 'image', 'genre', 'console']

class GameUpdateView(CreateView):
	model = Game

class GameDeleteView(CreateView):
	model = Game
