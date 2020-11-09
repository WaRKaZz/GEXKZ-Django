from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    UpdateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from gameexch.models import Comment
from .models import Profile
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Your account {username} has been created you are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,
                             'Your account  has been updated!')
            return redirect('profile-edit')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit.html', context)


@login_required
def profile_moderation(request, profile_id):
    if request.user.profile.rules == 'M' or request.user.profile.rules == 'A':
        instance = get_object_or_404(Profile, pk=profile_id)
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=instance.user)
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=instance)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,
                                 f'Account  has been updated!{instance.user.username}')
                return redirect('profile-view', pk=profile_id)
        else:
            u_form = UserUpdateForm(instance=instance)
            p_form = ProfileUpdateForm(instance=instance)
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'object': instance,
        }
        return render(request, 'users/profile_moderation.html', context)
    else:
        raise PermissionDenied


class ProfileDetailView(DetailView):

    model = Profile
    template_name = 'users/profile_view.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            message = request.POST.get('message')
            comment = Comment.objects.create(user=self.user.get_object().user,
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
        context['comments'] = Comment.objects.filter(
            user=self.get_object().user).order_by('-id')
        context['comment_form'] = CommentForm
        return context


class ProfileBanView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'users/profile_form.html'
    fields = ['banned', 'ban_commentary']

    def test_func(self):
        if (self.get_object().rules == 'M' or self.get_object().rules == 'A'):
            return False
        else:
            return (self.request.user.profile.rules == 'M' or self.request.user.profile.rules == 'A')


class ProfileRulesChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'users/profile_form.html'
    fields = ['rules']

    def test_func(self):
        return self.request.user.profile.rules == 'A'
