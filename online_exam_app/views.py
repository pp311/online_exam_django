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
from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_enumerate(value):
    return enumerate(value)
@register.filter
def to_str(value):
    return str(value)
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
                return redirect('/test-list')
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
        list_multichoice = request.POST.getlist('cb')
        multichoice_question_index = 0
        for i in range(1, number_of_questions + 1):
            statements = request.POST.getlist('txt' + str(i))
            if list_multichoice != None and len(list_multichoice) > multichoice_question_index and int(list_multichoice[multichoice_question_index]) == i:
                current_question = Question.objects.create(Test=test, Content=statements[0], MultipleChoice=True)
                multichoice_question_index += 1
                cb_answers = request.POST.getlist('cb' + str(i))
                k = 0
                for j in range(1, len(statements)):
                    is_correct = False
                    if len(cb_answers) > k and int(cb_answers[k]) == j:
                        is_correct = True
                        k += 1 
                    Answer.objects.create(Question=current_question, Content=statements[j], IsCorrectAnswer=is_correct)
            else:
                current_question = Question.objects.create(Test=test, Content=statements[0], MultipleChoice=False)
                answer = request.POST['group' + str(i)]
                for j in range(1, len(statements)):
                    is_correct = False
                    if int(answer) == j:
                        is_correct = True
                    Answer.objects.create(Question=current_question, Content=statements[j], IsCorrectAnswer=is_correct)
        return redirect('/test-list')

class DoTestPageView(View):
    template_name = 'do_test.html'
    def get(self, request):
        test_id = request.GET['id-test']
        test = Test.objects.get(IDTest=test_id)
        questions = Question.objects.filter(Test=test)
        answers = Answer.objects.filter(Question__in=questions).values()
        questions = questions.values()
        return render(request, self.template_name, {'test': test, 'questions': questions, 'answers': answers})
    def post(self, request):
        test_id = request.GET['id-test']
        submit_time = datetime.datetime.now()
        test = Test.objects.get(IDTest=test_id)
        questions = Question.objects.filter(Test=test)
        result = Result.objects.create(Test=test, User=User.objects.get(username=request.session['username']), SubmitTime=submit_time, Grade=0)
        grade = 0.0
        scd = 0.0
        for question in questions:
            if not question.MultipleChoice:
                answer = int(request.POST['group' + str(question.IDQuestion)])
                answer_obj = Answer.objects.get(IDAnswer=answer)
                if answer_obj.IsCorrectAnswer:
                    scd += 1
                result.History.add(answer_obj)
            else:
                list_answer = request.POST.getlist('cb' + str(question.IDQuestion))
                correct_answer_count = Answer.objects.filter(Question=question, IsCorrectAnswer=True).count()
                dung = 0.0
                for answer in list_answer:
                    answer_obj = Answer.objects.get(IDAnswer=int(answer))
                    if answer_obj.IsCorrectAnswer:
                        dung += 1/correct_answer_count
                    else:
                        dung -= 1/correct_answer_count
                    result.History.add(answer_obj)
                    print(dung)
                if dung > 0:
                    scd += dung

        grade = scd / questions.count() * 10
        print(scd)
        result.Grade = grade
        result.save() 
        return redirect('/result/?id-result=' + str(result.IDResult))
        
        
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
    def get(self, request):
        id_result = request.GET.get('id-result')
        result = Result.objects.get(IDResult=id_result)
        return render(request,self.template_name, {'result':result})


class ViewTestAllStudentsPageView(View):
    template_name = 'view_test_all_students.html'
    def get(self, request):
        id_test = request.GET.get('id-test')
        test = Test.objects.get(IDTest=id_test)
        result_list = Result.objects.filter(Test=test)
        #id-test dau ra
        queryset = result_list.all()
        queryset_dict = [{'IDResult':item.IDResult,'Grade': item.Grade, 'SubmitTime': item.SubmitTime,'Name':UserProfile.objects.get(User=item.User).Name} for item in queryset]
        return render(request,self.template_name, {'result_list':result_list,'queryset_dict':queryset_dict})
class ViewDetailPageView(View):
    template_name = 'view_detail.html'
    def get(self, request):
        id_result = request.GET.get('id-result')
        result = Result.objects.get(IDResult=id_result)
        list_history = result.History.all()
        test = result.Test
        subject = test.Subject
        list_question = Question.objects.filter(Test=test)
        # list_question = [
        list_answer = Answer.objects.filter(Question__in=list_question).values()
        userprofile = UserProfile.objects.get(User=result.User)
        list_answer_history = []
        for i in range(len(list_history)):
            list_answer_history.append(str(list_history[i]))
        # print(str(list_history[0]))
        print(list_answer_history)
        return render(request,self.template_name, {'result':result,'list_history':list_answer_history,'test':test,'subject':subject,'list_question':list_question,'list_answer':list_answer,'userprofile':userprofile})
class DeleteTestPageView(View):
    template_name = 'test_list.html'
    def get(self, request):
        id_test = request.GET.get('id-test')
        test = Test.objects.get(IDTest=id_test)
        test.delete()
        return redirect('/test-list')
    