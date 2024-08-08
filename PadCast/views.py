from django.shortcuts import render,redirect,get_object_or_404
from .models import PrimeCast
from Account.models import Teacher
from App.models import Comment,Reply
from .forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
# Create your views here.


def index_primecast(request):
    md = PrimeCast.objects.filter(is_active=True).order_by("-date")
    return render(request,'primecast/index.html',{
        'md':md,
    })

def detail_padcast(request,slug):
    md = get_object_or_404(PrimeCast,slug=slug)
    comment_md = CommentCast.objects.filter(primecast=md, is_active=True)
    teacher = Teacher.objects.get(user=md.user)
    replies = {}
    for comment in comment_md:
        replies[comment.id] = ReplyCast.objects.filter(key=comment)

    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.primecast = md
                new_comment.save()
                messages.success(request, 'کامت شما بعد از تایید نمایش داده میشود', 'success')

                return redirect('detail_padcast', slug=md.slug)
        else:
            messages.error(request,'سید اول لاگین کن ','danger')
            return redirect('login')
    else:
        form = CommentForm()
    
    return render(request,'primecast/detail.html',{
        "md": md,
        "form": form,
        "comments": comment_md,
        "replies": replies,
        "teacher": teacher,
    })



@user_passes_test(lambda u: u.is_staff)
@login_required(login_url='/account/login/')
def create_primecast(request):
    if request.method == "POST":
        form = PrimecastForm(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            messages.success(request,f'مدرس عزیز {request.user} پرایم کست شما ساخته شد')
            return redirect("index")
    else:
        form = PrimecastForm()

    try:
        return render(request,'primecast/create_primecast.html',{
            "form":form,
        })
    except Teacher.DoesNotExist:
        messages.error(request,'شما فاقد پروفایل میباشید لطفا اول پروفایل بسازید','danger')
        return redirect("create_profile")
