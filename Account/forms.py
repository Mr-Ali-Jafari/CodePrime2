from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

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