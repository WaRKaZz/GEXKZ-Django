from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
	u_form = UserUpdateForm()
	p_form = ProfileUpdateForm()
	
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	
	return render(request, 'users/edit.html', context)
