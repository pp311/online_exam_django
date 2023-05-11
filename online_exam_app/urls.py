
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('', views.main, name='main'),
    path('create-account/', views.CreateAccountPageView.as_view(), name='create_account'),
]
