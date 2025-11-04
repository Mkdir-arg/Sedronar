from django.apps import AppConfig


class LegajosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'legajos'
    
    def ready(self):
        import legajos.signals_historial
    
    def ready(self):
        import legajos.signals_alertas
    verbose_name = 'Legajos'