from django.apps import AppConfig
import requests

class PlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Platform'
    
    def ready(self):
        import Platform.signals


