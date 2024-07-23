from django import forms
from .models import Purchase,Comment,Reply

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
            "text":forms.Textarea(attrs={"class":"form-control"})
        }