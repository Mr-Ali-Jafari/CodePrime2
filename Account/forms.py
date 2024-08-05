from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from . import models
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            'min_length': 'پسورد باید حداقل ۸ کاراکتر باشد.'
        }
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            'min_length': 'پسورد تایید باید حداقل ۸ کاراکتر باشد.'
        }
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('پسورد باید حداقل ۸ کاراکتر باشد.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('پسورد و تایید پسورد باید یکسان باشند.')
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            'min_length': 'پسورد باید حداقل ۸ کاراکتر باشد.'
        }
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('پسورد باید حداقل ۸ کاراکتر باشد.')
        return password
    


class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        exclude = ["user"]

        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "family":forms.TextInput(attrs={"class":"form-control"}),
            "biography":forms.Textarea(attrs={"class":"form-control"}),
            "birthday":forms.DateInput(attrs={"class":"form-control","type":"date"}),


            "city":forms.TextInput(attrs={"class":"form-control"}),
            "picture":forms.FileInput(attrs={"class":"form-control"}),



        }

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = models.Participation
        exclude = ["user"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام خود را وارد کنید",
                "aria-label": "نام"
            }),
            "family": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی خود را وارد کنید",
                "aria-label": "نام خانوادگی"
            }),
            "number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "شماره تماس خود را وارد کنید",
                "aria-label": "شماره تماس"
            }),
            "gender": forms.Select(attrs={
                "class": "form-control",
                "aria-label": "جنسیت"
            }),
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "شرح سوابق تحصیلی و کاری خود را وارد کنید",
                "aria-label": "شرح سوابق"
            }),
            "participate_type": forms.Select(attrs={
                "class": "form-control",
                "aria-label": "نوع همکاری"
            }),
            "birthday": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "aria-label": "تاریخ تولد"
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام شهر خود را وارد کنید",
                "aria-label": "شهر"
            }),
            "info_card": forms.FileInput(attrs={
                "class": "form-control",
                "aria-label": "آپلود مدارک"
            }),
        }