from django.apps import AppConfig


class JobApplicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.job_applications"

    def ready(self):
        import apps.job_applications.signals  # noqa
