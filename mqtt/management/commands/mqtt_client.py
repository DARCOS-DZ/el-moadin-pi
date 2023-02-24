from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    This command runs the RabbitMQ consumer
    """
    help = 'Run the RabbitMQ consumer'

    def handle(self, *args, **options):
        import mqtt.mqtt_client
        mqtt.mqtt_client.background_loop()
