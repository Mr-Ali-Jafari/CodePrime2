from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("user__username",'title',)
    list_filter = ('price','is_active','date')
    
@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ('is_active','date')

@admin.register(models.Video_Product)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ("title",'product__title')
    list_filter = ('is_active','date')



@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ("user__username",'package__title','date')


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    search_fields = ("user__username",'tracking_code')
    list_filter = ('is_active','purchase_date')



@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("product__title",'user__username')
    list_filter = ('is_active','date')



@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    search_fields = ("key__product__title",'user__username')
    list_filter = ('date',)
