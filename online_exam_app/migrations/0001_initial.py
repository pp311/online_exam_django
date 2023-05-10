# Generated by Django 4.2.1 on 2023-05-10 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('IDAnswer', models.AutoField(primary_key=True, serialize=False)),
                ('Content', models.TextField()),
                ('IsCorrectAnswer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('IDSubject', models.AutoField(primary_key=True, serialize=False)),
                ('SubjectName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('Gender', models.BooleanField()),
                ('Code', models.CharField(max_length=9)),
                ('Class', models.CharField(max_length=12)),
                ('Faculty', models.TextField()),
                ('Position', models.TextField()),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('IDTest', models.AutoField(primary_key=True, serialize=False)),
                ('DateTest', models.DateTimeField()),
                ('NumberQuestion', models.IntegerField()),
                ('Time', models.IntegerField()),
                ('TestName', models.TextField()),
                ('Name', models.CharField(max_length=255)),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_exam_app.subject')),
                ('User', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('IDResult', models.AutoField(primary_key=True, serialize=False)),
                ('Grade', models.FloatField()),
                ('SubmitTime', models.DateTimeField()),
                ('History', models.ManyToManyField(to='online_exam_app.answer')),
                ('Test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_exam_app.test')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('IDQuestion', models.AutoField(primary_key=True, serialize=False)),
                ('Content', models.TextField()),
                ('MultipleChoice', models.BooleanField()),
                ('Test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_exam_app.test')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='Question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_exam_app.question'),
        ),
    ]
