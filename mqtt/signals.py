from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
import json
from datetime import datetime


@receiver(post_save, sender=Job)
def message_signal(sender, instance, **kwargs):
    if instance.sender == 0 :
        from . import mqtt
        json_form = """
{
     "sender": 0,
     "chron": """ + '\"' + instance.chron + "\"" + """,
     "audio": """ + '\"' + instance.audio + "\"" + """
}"""
        mqtt.client.publish(str(instance.topic),json_form)
        now = datetime.now()
        print(now, "\nFrom Topic: {} \nAudio file path: {} \nIs scheduled for: {} \npublished by: {}".format(instance.topic, instance.audio, instance.chron, instance.sender))
    else :
        pass
