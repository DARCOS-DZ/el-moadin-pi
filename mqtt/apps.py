from django.apps import AppConfig
import time

class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"
    def ready(self):
        from el_moadin_pi.utils import background_loop
        background_loop()
