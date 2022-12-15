from django.apps import AppConfig


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"
    def ready(self):
        from . import (mqtt_client, signals)
        client = mqtt_client.main()
        client.loop_start()
