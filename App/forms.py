from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['payment_receipt', 'payment_sms', 'desc']
        widgets = {
            'desc': forms.Textarea(attrs={'class': "form-control"}),
            'payment_receipt':forms.FileInput(attrs={'class': "form-control"}),
            'payment_sms':forms.FileInput(attrs={'class': "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['is_active','user','product']
        
        widgets = {
            "text":forms.Textarea(attrs={"class":"form-control"})
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ['user', 'key']

        widgets = {
            "text":CKEditorWidget(),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['user']
        
        widgets = {
            "desc":forms.Textarea(attrs={"class":"form-control"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "img":forms.FileInput(attrs={"class":"form-control"}),

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user']
        
        widgets = {
            "desc":forms.Textarea(attrs={"class":"form-control"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "slug":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),


            "intro":forms.FileInput(attrs={"class":"form-control"}),
            "img":forms.FileInput(attrs={"class":"form-control"}),



        }



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video_Product
        exclude = ['user','product']
        
        widgets = {
            "desc":forms.Textarea(attrs={"class":"form-control"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),


            "video":forms.FileInput(attrs={"class":"form-control"}),



        }
