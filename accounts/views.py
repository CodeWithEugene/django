from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, FarmerProfileForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, f'Account created! You can now login.')
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
    })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'accounts/update_profile.html', context)