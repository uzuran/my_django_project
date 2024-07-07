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
    """Class for allowed to multiply selection."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    A custom form field for handling multiple file uploads.

    This class extends Django's FileField to support multiple file uploads. It uses
    a custom widget, `MultipleFileInput`, to allow selecting multiple files at once.
    The clean method is overridden to handle and validate each file individually if
    multiple files are uploaded.

    Methods:
    --------
    __init__(*args, **kwargs):
        Initializes the field with the custom widget for multiple file input.

    clean(data, initial=None):
        Cleans and validates each file in the input data. If multiple files are
        provided, it returns a list of cleaned files. If a single file is provided,
        it returns the cleaned file.

    Parameters:
    -----------
    *args : tuple
        Variable length argument list.
    **kwargs : dict
        Arbitrary keyword arguments.

    Attributes:
    -----------
    widget : MultipleFileInput
        The widget used for rendering the input field, set to allow multiple file
        selection.
    """
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
    """Upload file form."""
    file = MultipleFileField(label='Select files', required=False)
