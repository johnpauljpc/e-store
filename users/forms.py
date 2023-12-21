from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserModel

class SignupForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("first_name", "other_names", "email",)

class LoginForm(Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)