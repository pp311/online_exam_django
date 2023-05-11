from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import LoginForm, CreateUserForm
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
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                is_superuser = user.is_superuser
                request.session['username'] = username
                request.session['position'] = 'admin' if is_superuser else 'user'
                request.session['name'] = user.userprofile.Name
                request.session.modified = True
                return redirect('/')
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Invalid form")

class CreateAccountPageView(FormView):
    template_name = 'create_account.html'
    form_class = CreateUserForm
    success_url = '/create-account/?err=0&success=1'
    error_url = '/create-account/?err=0&success=0'
    def form_valid(self, form):
        print("haha")
        if User.objects.filter(username=form.cleaned_data["username"]).exists():
            return redirect('/create-account/?err=1')
        if UserProfile.objects.filter(Code=form.cleaned_data["code"]).exists():
            return redirect('/create-account/?err=2')
        print("hehe")
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
