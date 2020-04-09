from django.shortcuts import render
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import(
	LoginRequiredMixin, 
	UserPassesTestMixin
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

class GameCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Game
	fields = ['name', 'description', 'image', 'genre', 'console']
	
	def test_func(self):
		return (self.request.user.profile.rules == 'M' 
		or self.request.user.profile.rules == 'A')

class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Game
	fields = ['name', 'description', 'image', 'genre', 'console']
	
	def test_func(self):
		return (self.request.user.profile.rules == 'M' 
		or self.request.user.profile.rules == 'A')

class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Game
	success_url = '/'
	
	def test_func(self):
		return (self.request.user.profile.rules == 'M' 
		or self.request.user.profile.rules == 'A')

