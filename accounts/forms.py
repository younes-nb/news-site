from django import forms
from django.forms.widgets import EmailInput, PasswordInput


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'login-input'}), label="نام کاربری ")
    password = forms.CharField(max_length=50, widget=PasswordInput(
        attrs={'class': 'login-input'}), label="رمز عبور ")


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=30,
                               widget=forms.TextInput(attrs={'class': 'login-input'}),
                               label="نام کاربری ")
    password = forms.CharField(required=True, max_length=50, min_length=8, widget=PasswordInput(
        attrs={'class': 'login-input'}), label="رمز عبور ")
    email = forms.EmailField(max_length=50, widget=EmailInput(
        attrs={'class': 'login-input'}), label="ایمیل ")
