from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(max_length=60,help_text='')
    class Meta:
        model=Account
        fields=['username','email','password1','password2',]
        '''
        widgets={
            "email":forms.EmailInput(
                attrs={'type':"email", 'placeholder':"Your Email"}),
            "password1":forms.PasswordInput(
                attrs={'type':"password"  ,'placeholder':"Password"}),
            'username':forms.TextInput(
                attrs={'type':"text",'placeholder':"Your Name"}),
            "password2": forms.PasswordInput(
                attrs={'type': "password",'placeholder': "Repeat your password"})
        }
        '''

class LoginForm(forms.Form):
    class Meta:
        fields=['email','password1']
        widgets={
            'email':forms.TextInput(
                attrs={'type':"email" ,'placeholder':"Your mail"}),
            'password1':forms.PasswordInput(
                attrs={'type':"password"   ,'placeholder':"Password"})
            }
