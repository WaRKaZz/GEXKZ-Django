from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='gex-home'),
	path('about/', views.about, name='gex-about')
]