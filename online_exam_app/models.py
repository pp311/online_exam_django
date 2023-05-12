from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.TextField(null=True)
    Gender = models.BooleanField(null=True)
    Code = models.CharField(max_length=9, null=True)
    Class = models.CharField(max_length=12, null=True)
    Faculty = models.TextField(null=True)
    Position = models.TextField(null=True)


class Subject(models.Model):
    IDSubject = models.AutoField(primary_key=True)
    SubjectName = models.TextField()
    def __str__(self):
        return self.SubjectName

class Test(models.Model):
    IDTest = models.AutoField(primary_key=True)
    DateTest = models.DateTimeField()
    NumberQuestion = models.IntegerField()
    Time = models.IntegerField()
    TestName = models.TextField()
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.TestName
    
class Question(models.Model):
    IDQuestion = models.AutoField(primary_key=True)
    Content = models.TextField()
    MultipleChoice = models.BooleanField()
    Test = models.ForeignKey(Test, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.IDQuestion)
    
class Answer(models.Model):
    IDAnswer = models.AutoField(primary_key=True)
    Content = models.TextField()
    IsCorrectAnswer = models.BooleanField()
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Question.IDQuestion) + " " + str(self.IDAnswer)

class Result(models.Model):
    IDResult = models.AutoField(primary_key=True)
    Grade = models.FloatField()
    SubmitTime = models.DateTimeField()
    Test = models.ForeignKey(Test, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    History = models.ManyToManyField(Answer)
