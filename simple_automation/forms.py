"""Forms for login"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """Sign up form"""
    class Meta:
        """Meta"""
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
