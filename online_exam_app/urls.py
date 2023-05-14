
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('', views.main, name='main'),
    path('create-account/', views.CreateAccountPageView.as_view(), name='create_account'),
    path('personal-info/', views.PersonalInfoPageView.as_view(), name='personal_info'),
    path('logout/', views.logOut.as_view(), name='logout'),
    path('create-test/', views.CreateTestPageView.as_view(), name='create_test'),
    path('test-list/', views.TestListPageView.as_view(), name='test_list'),
    path('history/', views.HistoryDoTestPageView.as_view(), name='history'),
    path('result/', views.ResultTestPageView.as_view(), name='result'),
    path('view-test-all-students/', views.ViewTestAllStudentsPageView.as_view(), name='view_test_all_students'),
]
