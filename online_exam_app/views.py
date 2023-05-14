from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import UserProfile, Subject, Test, Question, Answer
from .models import UserProfile,Test, Result
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import LoginForm, CreateUserForm, PersonalInfoForm
import datetime
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


class CreateTestPageView(View):
    template_name = 'create_test.html'
    def get(self, request):
        subject_list = Subject.objects.all().values()
        current_datetime = current_datetime=datetime.datetime.today().strftime("%Y-%m-%dT%H:%M")
        return render(request, self.template_name, {'subject_list': subject_list, 'current_datetime': current_datetime})
    def post(self, request):
        test_name = request.POST['test-name']
        subject_id = int(request.POST['subject-test']) 
        date_test = request.POST['date-test']
        time_test = int(request.POST['time-in-minutes'])
        number_of_questions = int(request.POST['number-of-questions'])
        
        user = User.objects.get(username=request.session['username'])
        subject = Subject.objects.get(IDSubject=subject_id)

        test = Test.objects.create(User=user, Subject=subject, TestName=test_name, DateTest=date_test, Time=time_test, NumberQuestion=number_of_questions)
        list_question = []
        list_answer = []
        list_multichoice = request.POST.getlist('cb')
        h = 0
        for i in range(number_of_questions):
            statements = request.POST.getlist('txt' + str(i+1))
            if list_multichoice != None and len(list_multichoice) > h and int(list_multichoice[h]) == i+1:
                list_question.append(Question.objects.create(Test=test, Content=statements[0], MultipleChoice=True))
                h += 1
                cb_answers = request.POST.getlist('cb' + str(i+1))
                k = 0
                for j in range(1, len(statements)):
                    is_correct = False
                    if len(cb_answers) > k and int(cb_answers[k]) == j:
                        is_correct = True
                        k += 1 
                    list_answer.append(Answer.objects.create(Question=list_question[i], Content=statements[j], IsCorrectAnswer=is_correct))
            
            else:
                list_question.append(Question.objects.create(Test=test, Content=statements, MultipleChoice=False))
                answer = request.POST['group' + str(i+1)]
                for j in range(1, len(statements)):
                    is_correct = False
                    if int(answer) == j:
                        is_correct = True
                    list_answer.append(Answer.objects.create(Question=list_question[i], Content=statements[j], IsCorrectAnswer=is_correct))

        
class TestListPageView(View):
    template_name = 'test_list.html'
    def get(self, request): 
        user_action = "Làm bài" if request.session['position'] == 'student' else 'Xem chi tiết'
        test_list = Test.objects.all().values()
        return render(request, self.template_name, {'user_action':user_action,'test_list':test_list})
class HistoryDoTestPageView(View):
    template_name = 'history_do_test.html'
    def get(self, request):
        user = User.objects.get(username=request.session['username'])
        result_list = Result.objects.filter(User=user)
        return render(request,self.template_name,{'user':user,'result_list':result_list})
class ResultTestPageView(View):
    template_name = 'result_test.html'
    def get(self, request):# r bh sua cai j day
        result = Result.objects.filter(User=User.objects.get(username=request.session['username']))
        #result = Result.objects.filter(Test=test)
        history = result.History.all().values()
        return render(request,self.template_name, {'result':result,'history':history})
class ViewTestAllStudentsPageView(View):
    template_name = 'view_test_all_students.html'
    def get(self, request):
        id_test = request.GET.get('id-test')
        test = Test.objects.get(IDTest=id_test)
        result_list = Result.objects.filter(Test=test)
        #id-test dau ra
        return render(request,self.template_name, {'result_list':result_list})