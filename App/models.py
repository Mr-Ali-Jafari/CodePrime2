from django.db import models
from django.contrib.auth.models import User
from persiantools.jdatetime import JalaliDate
from ckeditor.fields import RichTextField

# Create your models here.





class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=1000)
    intro = models.FileField(upload_to="intro/product/%Y/")
    img = models.ImageField(upload_to="banners/product/%Y/")
    desc = RichTextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    price = models.IntegerField()
    categories = models.ForeignKey(Category, related_name='products', blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"Title: {self.title} - Who Published: {self.user.username} - date: {JalaliDate(self.date)} - Active ? {self.is_active}"
    


class Video_Product(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    video = models.FileField(upload_to='videos/%Y/')
    desc = RichTextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Title: {self.title} - Who Published: {self.product.user.username} - date: {JalaliDate(self.date)} - Active ? {self.is_active} - For: {self.product.title}"


class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    img = models.ImageField(upload_to="banners/product/%Y/")
    desc = RichTextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Title: {self.title} - Who Published: {self.user.username} - date: {JalaliDate(self.date)} - Active ? {self.is_active}"
    




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.title} - << {JalaliDate(self.date)} >>"
    



class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey('Product', on_delete=models.CASCADE)
    payment_receipt = models.ImageField(upload_to='receipts/%Y')
    payment_sms = models.ImageField(upload_to="sms/payment/%Y")
    desc = models.TextField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    tracking_code = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.package.title} - {self.purchase_date} < +- کدپیگیری : {self.tracking_code} -+ >"
    



class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - Active?{self.is_active}"
    





class Reply(models.Model):    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    key = models.ForeignKey(Comment,on_delete=models.CASCADE, related_name='replies')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.key.product.title}"