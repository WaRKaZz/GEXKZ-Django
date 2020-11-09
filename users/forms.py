from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from gameexch.models import Comment


class CheckBannedAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        print(user.profile.banned)
        if user.profile.banned:
            raise forms.ValidationError('This account banned',
                                        code='banned'
                                        )


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['image', 'vk', 'city', 'about', 'phone',
                  'whatsapp', 'telegram']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', ]
