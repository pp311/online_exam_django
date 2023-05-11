from django.apps import AppConfig


class OnlineExamAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_exam_app'

    # def ready(self):
    #     import online_exam_app.signals
