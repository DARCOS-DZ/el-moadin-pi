from django.apps import AppConfig
import os

class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from . import signals, mqtt_client
            from django.core.management import call_command
            client = mqtt_client.main()
            client.loop_start()
