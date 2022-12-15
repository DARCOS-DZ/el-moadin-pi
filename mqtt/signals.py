from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
import json
from datetime import datetime


@receiver(post_save, sender=Job)
def message_signal(sender, instance, **kwargs):
    if instance.sender == 0 :
        from . import mqtt_publisher
        json_form = """
{
     "sender": 0,
     "chron": """ + '\"' + instance.chron + "\"" + """,
     "audio": """ + '\"' + instance.audio + "\"" + """
}"""
        mqtt_publisher.main(topic=str(instance.topic), message=json_form)
        now = datetime.now()
        print(str(now), "Topic: {} / Message-POST: {} published-by: {}".format(instance.topic, instance.chron, instance.sender))
    else :
        pass
