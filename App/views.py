from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import random
from .forms import *
# Create your views here.

def index(request):
    md = models.Product.objects.all().order_by("-date")[:3]
    blog = models.Blog.objects.all().order_by("-date").filter(is_active=True)[:3]

    context = {
        "md":md,
        'blog':blog,
    }
    return render(request,'app/index.html',context=context)


def all_package(request):
    search_query = request.GET.get('search', '')  
    model = models.Product.objects.all().order_by('-date')

    if search_query:
        model = model.filter(title__icontains=search_query)
    


    return render(request, 'app/all_pkg.html', {'md': model, 'search_query': search_query})

def all_blog(request):
    blog = models.Blog.objects.all().order_by("-date").filter(is_active=True)

    context = {
        "blog":blog,

    }
    return render(request,'app/all_blog.html',context=context) 

@login_required(login_url='/account/login/')
def purchase_history(request):
    md = models.Product.objects.all()
    p = models.Purchase.objects.filter(user=request.user,package__in=md,is_active=True)
    context = {
        "p":p,
    }
    return render(request,'app/purchase_history.html',context=context)



def detail(request, slug):
    md = get_object_or_404(models.Product, slug=slug)
    p = models.Purchase.objects.filter(package=md)
    comment_md = models.Comment.objects.filter(product=md, is_active=True)
    vid = models.Video_Product.objects.filter(product=md, is_active=True)

    replies = {}
    for comment in comment_md:
        replies[comment.id] = models.Reply.objects.filter(key=comment)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = md
            if request.user.is_authenticated:
                new_comment.save()
                messages.success(request,'کامت شما بعد از تایید نمایش داده میشود ','success')

                return redirect('detail', slug=md.slug)
            else:
                messages.error(request,'سید شما هنوز لاگین نکردید ','danger')
                return redirect("index")
    else:
        form = CommentForm()

    context = {

        "md": md,
        "vid": vid,
        "p": p,
        "form": form,
        "comments": comment_md,
        "replies": replies,
    }

    return render(request, 'app/detail_product.html', context=context)


def blog_detail(request,pk):
    md = models.Blog.objects.get(pk=pk)
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

    if p_exists or get_object_or_404(models.Product,pk=pk).user == request.user:
        video = get_object_or_404(models.Video_Product, pk=pk)
    else:
        messages.error(request,'داداش ما بیایم وقت بزاریم و دوره درست کنیم شما بیای پولم بالاش ندی | جهت شوخی بود اگه میخوای دوره در دسترس هستش حتما بخرش','danger')
        return redirect('index')
    
    context = {
        "vid":video,
    }

    return render(request,'app/detail_vid.html',context=context)


@login_required(login_url='/account/login/')
def view_cart(request):
    cart_items = models.CartItem.objects.filter(user=request.user)
    total_price = sum(item.package.price for item in cart_items)
    
    
    
    return render(request, 'app/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='/account/login/')
def add_to_cart(request, pk):
    package = get_object_or_404(models.Product, pk=pk,is_active=True)
    cart_item_exists = models.CartItem.objects.filter(user=request.user, package=package).exists()
    
    if cart_item_exists:
        messages.warning(request, "این محصول قبلاً به سبد خرید شما اضافه شده است.",'warning')
    else:
        models.CartItem.objects.create(user=request.user, package=package)
        messages.success(request, f"{package.title} به سبد خرید شما اضافه شد.",'success')
    
    return redirect('view_cart')

@login_required(login_url='/account/login/')
def remove_from_cart(request, pk):
    cart_item = models.CartItem.objects.get(pk=pk)
    cart_item.delete()
    messages.success(request, "ایتم مورد نظر از سبد شما حذف شد.",'success')
    return redirect('view_cart')


@user_passes_test(lambda u: u.is_superuser) 
def activate_purchase(request, purchase_id):
    purchase = get_object_or_404(models.Purchase, id=purchase_id)
    purchase.is_active = True
    purchase.save()
    return redirect('list_purchases')

@user_passes_test(lambda u: u.is_superuser)
def list_purchases(request):
    purchases = models.Purchase.objects.filter(is_active=False)
    return render(request, 'app/list_purchases.html', {'purchases': purchases})






@login_required(login_url='/account/login/')
def purchase(request, purchase_id):
    product = get_object_or_404(models.Product, id=purchase_id)
    cart_item = models.CartItem.objects.filter(package=product)
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