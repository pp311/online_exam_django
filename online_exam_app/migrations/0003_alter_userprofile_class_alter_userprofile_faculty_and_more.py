# Generated by Django 4.2.1 on 2023-05-11 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_exam_app', '0002_remove_test_user_test_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Class',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Faculty',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Gender',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Name',
            field=models.TextField(null=True),
        ),
    ]
