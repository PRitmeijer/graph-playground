from django.apps import AppConfig


class UserStatusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userstatus'

    def ready(self):
        #Implicitily conntect signal handlers decorated with @receiver
        import userstatus.signals
