from gameexch.models import Game, UserToGame, Comment
from django.contrib.auth import get_user


def game_methods_handler(request, method):
    game_pk = request.POST.get('game_pk')
    user = get_user(request)
    u2g, game = None, None
    if game_pk is not None:
        game = Game.objects.filter(
            pk=int(game_pk)).first()
        u2g = UserToGame.objects.filter(game=game, user=user).first()
        if u2g is None:
            u2g = UserToGame(game=game, user=user)
            u2g.save()
    if method == 'owner':
        if u2g.is_owner:
            u2g.is_owner = False
        else:
            u2g.is_owner = True
            u2g.is_wanted = False
        u2g.save()
    elif method == 'whishlist':
        if u2g.is_wanted:
            u2g.is_wanted = False
        else:
            u2g.is_owner = False
            u2g.is_wanted = True
        u2g.save()
    elif method == 'like':
        if u2g.is_like:
            game.likes -= 1
        else:
            game.likes += 1
        u2g.is_like = not u2g.is_like
        u2g.save()
        game.save()
    elif method == 'comment_like':
        comment = Comment.objects.filter(
            pk=int(request.POST.get('comment_pk'))).first()
        print(type(comment))
        if user in comment.liked_by.all():
            comment.likes -= 1
            comment.liked_by.remove(user)
            print('dislike')
        else:
            print('like')
            comment.likes += 1
            comment.liked_by.add(user)
        comment.save()
