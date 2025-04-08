from django.apps import AppConfig

class TalentrackerConfig(AppConfig):  # Cambia el nombre de WaConfig a TalentrackerConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talentracker'
    
    def ready(self):
        # Importa las señales para que se registren
     import talentracker.signals