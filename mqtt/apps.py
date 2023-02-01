from django.apps import AppConfig
import time
import background

class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"
    @background.task
    def ready(self):
        import mqtt.mqtt_client
        mqtt.mqtt_client.background_loop()
