from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    username.label = ""
    password.label = ""
    class Meta:
        fields = ['username', 'password']


class CreateUserForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mã sinh viên'})) 
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    position = forms.ChoiceField(choices=[('teacher', 'Giáo viên'), ('student', 'Sinh viên')])
    username.label = "Tên đăng nhập"
    password.label = "Mật khẩu"
    code.label = "Mã sinh viên"
    position.label = "Vị trí"

