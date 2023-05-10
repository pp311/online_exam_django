from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.TextField()
    Gender = models.BooleanField()
    Code = models.CharField(max_length=9)
    Class = models.CharField(max_length=12)
    Faculty = models.TextField()
    Position = models.TextField()

class Subject(models.Model):
    IDSubject = models.AutoField(primary_key=True)
    SubjectName = models.TextField()

class Test(models.Model):
    IDTest = models.AutoField(primary_key=True)
    DateTest = models.DateTimeField()
    NumberQuestion = models.IntegerField()
    Time = models.IntegerField()
    TestName = models.TextField()
    Name = models.CharField(max_length=255)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Question(models.Model):
    IDQuestion = models.AutoField(primary_key=True)
    Content = models.TextField()
    MultipleChoice = models.BooleanField()
    Test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Answer(models.Model):
    IDAnswer = models.AutoField(primary_key=True)
    Content = models.TextField()
    IsCorrectAnswer = models.BooleanField()
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Result(models.Model):
    IDResult = models.AutoField(primary_key=True)
    Grade = models.FloatField()
    SubmitTime = models.DateTimeField()
    Test = models.ForeignKey(Test, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    History = models.ManyToManyField(Answer)
