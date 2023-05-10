from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    username.label = ""
    password.label = ""
    class Meta:
        fields = ['username', 'password']
