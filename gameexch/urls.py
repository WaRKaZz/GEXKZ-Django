from django.urls import path
from .views import (
    GameListView,
    GameDetailView,
    GameCreateView,
    GameUpdateView,
    GameDeleteView,
    CommentDeleteView
)
from . import views

urlpatterns = [
    path('', GameListView.as_view(), name='gex-game-view'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='gex-game-datail'),
    path('game/new', GameCreateView.as_view(), name='gex-game-create'),
    path('game/<int:pk>/update',
         GameUpdateView.as_view(),
         name='gex-game-update'),
    path('game/<int:pk>/delete',
         GameDeleteView.as_view(),
         name='gex-game-delete'),

    path('game/comment/<int:pk>/delete', CommentDeleteView.as_view(),
         name='gex-game-comment-delete'),
]
