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
    template_name = "gameexch/game_object/game_list.html"
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
    template_name = "gameexch/game_object/game_detail.html"
    model = Game

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
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
            elif method in ('owner', 'whishlist', 'like', 'comment_like'):
                game_methods_handler(request, method)
            else:
                messages.error(request, comment_form.errors.as_text()[10:])
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
    template_name = "gameexch/game_object/game_form.html"
    model = Game
    fields = ['name', 'image', 'genre', 'platform']

    def test_func(self):
        return (self.request.user.profile.rules == 'M'
                or self.request.user.profile.rules == 'A')


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "gameexch/game_object/game_form.html"
    model = Game
    fields = ['name', 'image', 'genre', 'platform']

    def test_func(self):
        return (self.request.user.profile.rules == 'M'
                or self.request.user.profile.rules == 'A')


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "gameexch/game_object/game_confirm_delete.html"
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
        print('laga')
        return reverse('gex-game-datail',
                       kwargs={'pk': self.get_object().game.id})

    def test_func(self):
        return ((self.get_object().author.profile.rules == 'U'
                 and self.request.user.profile.rules == 'M')
                or self.request.user.profile.rules == 'A'
                or self.request.user == self.get_object().author)
