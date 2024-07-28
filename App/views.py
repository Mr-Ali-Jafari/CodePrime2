from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from . import models as model_file
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import random
from .forms import *
from django.conf import settings
import os
# Create your views here.



def robots_txt(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'robots.txt')
    with open(file_path) as f:
        return HttpResponse(f.read(), content_type='text/plain')



def sitemap_xml(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'sitemap.xml')
    with open(file_path) as f:
        return HttpResponse(f.read(), content_type='text/xml')

def index(request):
    md = model_file.Product.objects.all().order_by("-date")[:3]
    blog = model_file.Blog.objects.all().order_by("-date").filter(is_active=True)[:3]

    context = {
        "md":md,
        'blog':blog,
    }
    return render(request,'app/index.html',context=context)


def all_package(request):
    search_query = request.GET.get('search', '')  
    model = model_file.Product.objects.all().order_by('-date')

    if search_query:
        model = model.filter(title__icontains=search_query)
    


    return render(request, 'app/all_pkg.html', {'md': model, 'search_query': search_query})

def all_blog(request):
    blog = model_file.Blog.objects.filter(is_active=True).order_by("-date")

    context = {
        "blog":blog,

    }
    return render(request,'app/all_blog.html',context=context) 

@login_required(login_url='/account/login/')
def purchase_history(request):
    md = model_file.Product.objects.all()
    p = model_file.Purchase.objects.filter(user=request.user,package__in=md,is_active=True)
    context = {
        "p":p,
    }
    return render(request,'app/purchase_history.html',context=context)



def detail(request, slug):
    md = get_object_or_404(model_file.Product, slug=slug)
    p = model_file.Purchase.objects.filter(package=md)
    count = model_file.Purchase.objects.filter(package=md,is_active=True).count()
    comment_md = model_file.Comment.objects.filter(product=md, is_active=True)
    vid = model_file.Video_Product.objects.filter(product=md, is_active=True)

    replies = {}
    for comment in comment_md:
        replies[comment.id] = model_file.Reply.objects.filter(key=comment)

    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.product = md
                new_comment.save()
                messages.success(request, 'کامت شما بعد از تایید نمایش داده میشود', 'success')

                return redirect('detail', slug=md.slug)
        else:
            messages.error(request,'سید اول لاگین کن ','danger')
            return redirect('login')
    else:
        form = CommentForm()


    context = {
        'student':count,
        "md": md,
        "vid": vid,
        "p": p,
        "form": form,
        "comments": comment_md,
        "replies": replies,
    }

    return render(request, 'app/detail_product.html', context=context)


def blog_detail(request,pk):
    md = model_file.Blog.objects.get(pk=pk)
    return render(request,"app/detail_blog.html",{
        "md":md,
    })

@user_passes_test(lambda u: u.is_superuser)
def send_reply(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.key = comment 
            new_reply.save()  
            return redirect('detail', slug=comment.product.slug) 

    else:
        form = ReplyForm()

    context = {
        "form": form
    }

    return render(request, "app/reply_admin.html", context=context)


@login_required(login_url='/account/login/')
def vid_detail(request,pk):
    p_exists = Purchase.objects.filter(user=request.user,is_active=True).exists()

    if p_exists or get_object_or_404(model_file.Product,pk=pk).user == request.user:
        video = get_object_or_404(model_file.Video_Product, pk=pk)
    else:
        messages.error(request,'داداش ما بیایم وقت بزاریم و دوره درست کنیم شما بیای پولم بالاش ندی | جهت شوخی بود اگه میخوای دوره در دسترس هستش حتما بخرش','danger')
        return redirect('index')
    
    context = {
        "vid":video,
    }

    return render(request,'app/detail_vid.html',context=context)


@login_required(login_url='/account/login/')
def view_cart(request):
    cart_items = model_file.CartItem.objects.filter(user=request.user)
    total_price = sum(item.package.price for item in cart_items)
    
    
    
    return render(request, 'app/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='/account/login/')
def add_to_cart(request, pk):
    package = get_object_or_404(model_file.Product, pk=pk,is_active=True)
    cart_item_exists = model_file.CartItem.objects.filter(user=request.user, package=package).exists()
    
    if cart_item_exists:
        messages.warning(request, "این محصول قبلاً به سبد خرید شما اضافه شده است.",'warning')
    else:
        model_file.CartItem.objects.create(user=request.user, package=package)
        messages.success(request, f"{package.title} به سبد خرید شما اضافه شد.",'success')
    
    return redirect('view_cart')

@login_required(login_url='/account/login/')
def remove_from_cart(request, pk):
    cart_item = model_file.CartItem.objects.get(pk=pk)
    cart_item.delete()
    messages.success(request, "ایتم مورد نظر از سبد شما حذف شد.",'success')
    return redirect('view_cart')


@user_passes_test(lambda u: u.is_superuser) 
def activate_purchase(request, purchase_id):
    purchase = get_object_or_404(model_file.Purchase, id=purchase_id)
    purchase.is_active = True
    purchase.save()
    return redirect('list_purchases')

@user_passes_test(lambda u: u.is_superuser)
def list_purchases(request):
    purchases = model_file.Purchase.objects.filter(is_active=False)
    return render(request, 'app/list_purchases.html', {'purchases': purchases})

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/account/login/')
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            messages.success(request,f'مدرس عزیز {request.user} پست شما ساخته شد')
            return redirect("index")
    else:
        form = BlogForm()

    return render(request,'app/create_blog.html',{
        "form":form,
    })



@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/account/login/')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            form.save()
            messages.success(request,f'مدرس عزیز {request.user} پکیح شما ساخته شد')
            return redirect("index")
    else:
        form = ProductForm()

    return render(request,'app/create_product.html',{
        "form":form,
    })




@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/account/login/')
def add_vid(request,pk):
    if request.method == "POST":
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.product = Product.objects.get(pk=pk)
            form.save()
            messages.success(request,f'مدرس عزیز {request.user} ویدیو شما اضافه شد')
            return redirect("index")
    else:
        form = VideoForm()

    return render(request,'app/add_vid.html',{
        "form":form,
    })


@login_required(login_url='/account/login/')
def purchase(request, purchase_id):
    product = get_object_or_404(model_file.Product, id=purchase_id)
    cart_item = model_file.CartItem.objects.filter(package=product)
    p = Purchase.objects.filter(user=request.user, package=product)
    if p.exists():
        messages.success(request,"درخواست شما ارسال شده حداقل 24 ساعت صبر کنید تا پکیج ارسال شود با تشکر | آکادمی کدپرایم","success")
        return redirect("index")
    if product.price == 0:
        purchase = Purchase(
            user=request.user,
            package=product,
            tracking_code=random.randint(0, 10000000),
            is_active=True
        )
        purchase.save()
        cart_item.delete()
        return redirect("detail",product.slug)
        
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.package = product
            purchase.tracking_code = random.randint(0,10000000)
            form.save()
            cart_item.delete()
            return redirect('index') 
    else:
        form = PurchaseForm()

    return render(request, 'app/purchase_package.html', {'product': product, 'form': form})


def custom_404(request, exception):
    return render(request, '404.html', status=404)