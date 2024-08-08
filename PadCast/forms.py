from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget



class PrimecastForm(forms.ModelForm):
    class Meta:
        model = PrimeCast
        exclude = ['user']

        widgets = {
            "desc":forms.Textarea(attrs={"class":"form-control"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "slug":forms.TextInput(attrs={"class":"form-control"}),

            "voice":forms.FileInput(attrs={"class":"form-control"}),
            "banner":forms.FileInput(attrs={"class":"form-control"}),
        }




class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentCast
        exclude = ['is_active','user','product']
        
        widgets = {
            "text":forms.Textarea(attrs={"class":"form-control"})
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = ReplyCast
        exclude = ['user', 'key']

        widgets = {
            "text":CKEditorWidget(),
        }
