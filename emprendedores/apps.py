from django.apps import AppConfig

class EmprendedoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emprendedores'

    def ready(self):
        import emprendedores.signals