from .forms import CommentForm
from .models import Game, Comment, UserToGame
from gameexch.common.util.options_handler import game_methods_handler
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def index(request):
    return render(request, 'gameexch/index.html', {'title': 'About'})


class GameListView(ListView):
    model = Game
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            method = request.POST.get('method')
            if method in ('owner', 'whishlist', 'like'):
                game_methods_handler(request, method)
        resonse = redirect('gex-game-view')
        if request.GET.get('page') is not None:
            resonse['Location'] += '?page=' + request.GET.get('page')
        return resonse


class GameDetailView(DetailView):
    model = Game

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST or None)
            print(comment_form.errors.as_text())
            if comment_form.is_valid():
                message = request.POST.get('message')
                comment = Comment.objects.create(game=self.get_object(),
                                                 author=request.user,
                                                 message=message)
                comment.save()
                messages.success(request,
                                 'Your massage was created!')
            else:
                messages.error(request, comment_form.errors.as_text()[5])

            method = request.POST.get('method')
            if method in ('owner', 'whishlist', 'like', 'comment_like'):
                game_methods_handler(request, method)

        return redirect('gex-game-datail', pk=self.get_object().id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        comments = Comment.objects.filter(game=game)
        paginator = Paginator(comments, 3)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['page_obj'] = page
        context['comment_form'] = CommentForm
        return context


class GameCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Game
    fields = ['name', 'image', 'genre', 'platform']

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


class CommentDeleteView(LoginRequiredMixin,
                        UserPassesTestMixin,
                        DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('gex-game-datail',
                       kwargs={'pk': self.get_object().game.id})

    def test_func(self):
        return ((self.get_object().author.profile.rules == 'U'
                 and self.request.user.profile.rules == 'M')
                or self.request.user.profile.rules == 'A'
                or self.request.user == self.get_object().author)
