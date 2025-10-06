from django.apps import AppConfig  # type: ignore


class JapapouConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "japapou"

    def ready(self):
        '''
            Método chamado quando o aplicativo é iniciado.
        '''
        import japapou.signals  # type: ignore
