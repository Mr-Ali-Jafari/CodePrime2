from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ParticipationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from .models import Teacher,Participation
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
            if user.is_staff:
                return redirect('create_profile')
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


@user_passes_test(lambda u: u.is_staff)
def create_or_edit_profile(request):
    try:
        profile = Teacher.objects.get(user=request.user)
        is_edit = True
    except Teacher.DoesNotExist:
        profile = None
        is_edit = False

    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request,f'مدرس گرامی {request.user} ورود شما را خوش آمد میگوییم از طرف بچه های کدپرایم!','success')
            return redirect('index')
    else:
        form = forms.TeacherForm(instance=profile)

    context = {
        'form': form,
    }
    
    return render(request, 'account/create_profile.html', context)




@login_required(login_url='/account/login/')
def create_participate(request):
    try:
        participate = Participation.objects.get(user=request.user)
    except Participation.DoesNotExist:
        participate = None

    if request.method == "POST":
        form = ParticipationForm(request.POST, request.FILES, instance=participate)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            messages.success(request, f'دوست عزیز {request.user.username} درخواست شما ارسال شد')
            return redirect("index")
        else:
            # چاپ خطاهای فرم برای عیب‌یابی
            print(form.errors)
    else:
        form = ParticipationForm(instance=participate)

    return render(request, 'account/participate.html', {
        "form": form,
    })