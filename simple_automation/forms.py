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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadFileForm(forms.Form):
    file = MultipleFileField(label='Select files', required=False)
