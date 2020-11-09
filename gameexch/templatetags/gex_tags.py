from django import template
from gameexch.models import UserToGame, Game
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def get_game_options(user_pk, game_pk):
    user = User.objects.filter(pk=user_pk).first()
    game = Game.objects.filter(pk=game_pk).first()
    return UserToGame.objects.filter(user=user, game=game).first()
