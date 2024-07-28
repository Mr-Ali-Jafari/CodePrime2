from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'اکانت شما با نام {username} ساخته شد!')
            return redirect('login')
    else:
        form = forms.CustomUserCreationForm()
    
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = forms.CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'خوش برگشتی، {user.username}!')
            return redirect('index')
    else:
        form = forms.CustomAuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    logout(request)
    messages.info(request, 'شما با موفقیت خارج شدید.')
    return redirect('index')
