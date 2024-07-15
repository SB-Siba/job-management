from django.apps import AppConfig


class AppCommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_common"

    def ready(self):
            import app_common.signals