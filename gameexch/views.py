from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import Game, GameComment
from .forms import GameCommentForm


def about(request):
    return render(request, 'gameexch/about.html', {'title': 'About'})


class GameListView(ListView):
    model = Game


class GameDetailView(DetailView):
    model = Game

    def post(self, request, *args, **kwargs):
        comment_form = GameCommentForm(request.POST or None)
        if comment_form.is_valid():
            message = request.POST.get('message')
            comment = GameComment.objects.create(game=self.get_object(),
                                                 author=request.user,
                                                 message=message)
            comment.save()
            messages.success(request,
                             'Your massage was created!')
            return redirect('gex-game-datail', pk=self.get_object().id)
        context = self.get_context_data()
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = GameComment.objects.filter(
            game=self.get_object()).order_by('-id')
        context['comment_form'] = GameCommentForm
        return context


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


class GameCommentDeleteView(LoginRequiredMixin,
                            UserPassesTestMixin,
                            DeleteView):
    model = GameComment

    def get_success_url(self):
        return reverse('gex-game-datail',
                       kwargs={'pk': self.get_object().game.id})

    def test_func(self):
        return ((self.get_object().author.profile.rules == 'U'
                 and self.request.user.profile.rules == 'M')
                or self.request.user.profile.rules == 'A'
                or self.request.user == self.get_object().author)
