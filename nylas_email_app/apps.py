from django.apps import AppConfig


class NylasEmailAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nylas_email_app'

    def ready(self):
        import nylas_email_app.signals
