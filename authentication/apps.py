from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
    def ready(self):
        # Import the signals module to ensure the signal handlers are registered
        import authentication.signals  # noqa: F401
        # The 'noqa: F401' comment is used to ignore the unused import warning
        # since we are not directly using anything from 'signals' in this file.