from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from constance.signals import config_updated
from datetime import datetime, timedelta
from .utils import get_todays_prayers
from constance import config
from django.core.files import File
import wget
from pathlib import Path
import json
from django.utils import timezone
from .tasks import prayer_event_task

@receiver(post_save, sender=LiveEvent)
def live_event_signal(sender, instance, **kwargs):
    audio = str(instance.audio)
    try:
        from .tasks import live_event_task
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
            live_event_task(id=instance.id,schedule=datetime.now() )

    except Exception as e:
        pass

@receiver(post_save, sender=PrayerAudio)
def prayer_audio_signal(sender, instance, **kwargs):
    audio = str(instance.audio)
    try:
        from .tasks import prayer_audio_task

        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()

    except Exception as e:
        pass

@receiver(post_save, sender=PrayerEvent)
def prayer_event_signal(sender, instance, **kwargs):
    audio = str(instance.audio)
    try:
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
        now = datetime.now()
        prayer = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), getattr(config, instance.prayer)), "%Y,%m,%d %H:%M:%S")
        delta = 10 + instance.audio_duration
        if instance.type == "before":
            schedule = prayer - timedelta(seconds=delta)
        else :
            schedule = prayer + timedelta(seconds=delta)
        print(schedule)
        prayer_event_task(id=instance.id,schedule=schedule)




    except Exception as e:
        pass

@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    print(sender, key, old_value, new_value)
    if key == "offset_time":
        try:
            prayer_source = config.PRAYER_SOURCE.replace("'", '"')
            prayer_source=json.loads(prayer_source)["data"]
        except Exception as e:
            prayer_source=config.PRAYER_SOURCE["data"]

        new_dictionary = {"data":[]}
        for prayer in prayer_source :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M')+timedelta(minutes=config.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary["data"].append(new_dictionary_item)
        config.PrayerTime = new_dictionary
        prayers = get_todays_prayers()
        config.elfajer = prayers["elfajer"]
        config.duhr = prayers["duhr"]
        config.alasr = prayers["alasr"]
        config.almaghreb = prayers["almaghreb"]
        config.alaicha = prayers["alaicha"]
