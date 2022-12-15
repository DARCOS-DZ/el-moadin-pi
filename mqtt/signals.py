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
     "msg": """ + '\"' + instance.chron + "\"" + """
}"""
        mqtt_publisher.main().publish(str(instance.topic),json_form)
        now = datetime.now()
        print(now, "Topic: {} / Message-POST: {} published-by: {}".format(instance.topic, instance.chron, instance.sender))
    else :
        pass
