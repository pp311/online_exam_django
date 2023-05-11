from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import LoginForm, CreateUserForm, PersonalInfoForm
# Create your views here.
def main(request):
  return HttpResponse("Home Page")

class LoginPageView(View):
    template_name = 'login.html'
    form_class = LoginForm
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = LoginForm(request, data=request.POST)
        #form  = self.form_class(request.POST)
        #form.is_valid()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_profile = UserProfile.objects.get(User=user)
                is_superuser = user.is_superuser
                request.session['username'] = username
                request.session['position'] = user_profile.Position
                request.session['name'] = user_profile.Name
                request.session.modified = True
                return redirect('/')
            else:
                return HttpResponse("Invalid username or password")
        else:
           return redirect('/login/?err=1')

class logOut(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        logout(request)
        return redirect('/login/')

class CreateAccountPageView(FormView):
    template_name = 'create_account.html'
    form_class = CreateUserForm
    success_url = '/create-account/?success=1'
    def form_valid(self, form):
        if User.objects.filter(username=form.cleaned_data["username"]).exists():
            return redirect('/create-account/?err=1')
        if UserProfile.objects.filter(Code=form.cleaned_data["code"]).exists():
            return redirect('/create-account/?err=2')
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        UserProfile.objects.create(
            User=user,
            Code=form.cleaned_data["code"],
            Position=form.cleaned_data["position"],
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        print("loi")

class PersonalInfoPageView(View):
    form_class = PersonalInfoForm
    template_name = 'personal_info.html'
    def get(self, request):
        err_msg = ''
        success_msg = ''
        if request.GET.get('err') == '1':
            err_msg = 'Xác nhận mật khẩu không khớp'
        elif request.GET.get('err') == '2':
            err_msg = 'Mật khẩu không chính xác'
        elif request.GET.get('success') == '1':
            success_msg = 'Cập nhật thông tin thành công'
        elif request.GET.get('success') == '2':
            success_msg = 'Đổi mật khẩu thành công'
        user = User.objects.get(username=request.session['username'])
        userprofile = UserProfile.objects.get(User=user)
        return render(request, self.template_name, {'personal_info_form': PersonalInfoForm(instance=userprofile), 'err_msg': err_msg, 'success_msg': success_msg})

    def post(self, request):
        if 'change-info-submit-btn' in request.POST:
            personal_info_form = PersonalInfoForm(request.POST, instance=UserProfile.objects.get(User=User.objects.get(username=request.session['username'])))
            if personal_info_form.is_valid():
                personal_info_form.save()
                return redirect('/personal-info/?success=1')
            else:
                return HttpResponse("Invalid form")
        elif 'change-password-submit-btn' in request.POST:
            #neu xac nhan mat khau khong khop
            if request.POST['new-password'] != request.POST['new-password2']:
                return redirect('/personal-info/?err=1')
            user = User.objects.get(username=request.session['username'])
            #neu mat khau khong chinh xac
            if not user.check_password(request.POST['current-password']):
                return redirect('/personal-info/?err=2')

            user.set_password(request.POST['new-password'])
            user.save()
            return redirect('/personal-info/?success=2')
