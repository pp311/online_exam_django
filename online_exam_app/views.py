from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import UserProfile
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import LoginForm
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
                return redirect('/')
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Invalid form")
