from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Se deshabilita carga automática de signals para evitar duplicaciones
        pass
        # import core.signals  ← DESACTIVADO
