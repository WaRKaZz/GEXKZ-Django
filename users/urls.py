"""GEXKZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CheckBannedAuthenticationForm
from users.views import (
    ProfileDetailView,
    ProfileBanView,
    ProfileRulesChangeView
)

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html',
                                      authentication_form=CheckBannedAuthenticationForm),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
    path('', user_views.profile, name='profile'),
    path('edit/', user_views.profile_edit, name='profile-edit'),
    path('<int:pk>', ProfileDetailView.as_view(), name='profile-view'),
    path('edit/<int:profile_id>',
         user_views.profile_moderation, name='profile-moderation'),
    path('ban/<int:pk>', ProfileBanView.as_view(), name='profile-ban'),
    path('rules/<int:pk>',
         ProfileRulesChangeView.as_view(), name='profile-rules'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
