from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    username.label = ""
    password.label = ""
    class Meta:
        fields = ['username', 'password']


class CreateUserForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mã sinh viên / giáo viên'})) 
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    position = forms.ChoiceField(choices=[('teacher', 'Giáo viên'), ('student', 'Sinh viên')])
    username.label = "Tên đăng nhập"
    password.label = "Mật khẩu"
    code.label = "Mã sinh viên"
    position.label = "Vị trí"

class PersonalInfoForm(forms.ModelForm):
    Code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mã sinh viên / giáo viên'})) 
    Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Họ và tên'})) 
    Class = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Lớp'}))
    Gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=[(True, 'Nam'), (False, 'Nữ')])
    Faculty = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Khoa'}))
    Code.label = "Mã sinh viên / giáo viên"
    Name.label = "Họ và tên"
    Class.label = "Lớp"
    Faculty.label = "Khoa"
    Gender.label = "Giới tính"
    class Meta:
        model = UserProfile
        fields = ('Name', 'Code', 'Class', 'Faculty', 'Gender')
