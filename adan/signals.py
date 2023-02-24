from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from constance.signals import config_updated
from datetime import datetime, timedelta
from constance import config
from django.core.files import File
import wget
from pathlib import Path
import json
from django.utils import timezone
from .tasks import prayer_event_task, live_event_task
import os

current_tz = timezone.get_current_timezone()

def downloader(instance, model="",current_tz=current_tz):
    # Don't perform any action if the instance has already been downloaded
    if instance.downloaded == False :
        # Download the audio file using wget
        audio = str(instance.audio)
        download  = wget.download(audio, out="media")
        downloaded_file = str(download)
        path = Path(downloaded_file)
        # Open the file and add it to the instance
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.downloaded = True
            instance.save()
            # Remove the downloaded file once it has been added to the instance
            os.remove(path)
        # Check what type of model the instance is and create a task to run at the appropriate time
        if model=="LiveEvent":
            live_event_task(id=instance.id,schedule=datetime.now(current_tz))
        if model=="PrayerEvent":
            # Get the prayer time from the config file
            now = datetime.now(current_tz)
            prayer = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), getattr(config, instance.prayer)), "%Y,%m,%d %H:%M:%S")
            # Calculate the time the task needs to run at
            delta = 10 + instance.audio_duration
            if instance.type == "before":
                schedule = prayer - timedelta(seconds=delta)
            else :
                schedule = prayer + timedelta(seconds=delta)
            # Create the task
            prayer_event_task(id=instance.id,schedule=schedule)

@receiver(post_save, sender=LiveEvent)
def live_event_signal(sender, instance, **kwargs):
    downloader(model="LiveEvent", instance=instance)

@receiver(post_save, sender=PrayerAudio)
def prayer_audio_signal(sender, instance, **kwargs):
    downloader(instance=instance)

@receiver(post_save, sender=PrayerEvent)
def prayer_event_signal(sender, instance, **kwargs):
    downloader(model="PrayerEvent", instance=instance)



@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    from adan.utils import get_todays_prayers
    print(sender, key, old_value, new_value)
    current_tz = timezone.get_current_timezone()
    if key == "offset_time":
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

# @receiver(config_updated)
# def constance_updated(sender, key, old_value, new_value, **kwargs):
#     from adan.utils import get_todays_prayers
#     print(sender, key, old_value, new_value)
#     current_tz = timezone.get_current_timezone()
#     if key == "offset_time":
#         prayer_source = config.PRAYER_SOURCE.get("data", None)
#
#         new_dictionary = {"data":[]}
#         offset_time_minutes = timedelta(minutes=config.offset_time)
#         for prayer in prayer_source :
#             elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M')+offset_time_minutes).time()
#             duhr=(datetime.strptime(prayer["duhr"], '%H:%M')+offset_time_minutes).time()
#             alasr=(datetime.strptime(prayer["alasr"], '%H:%M')+offset_time_minutes).time()
#             almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M')+offset_time_minutes).time()
#             alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M')+offset_time_minutes).time()
#             chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M')+offset_time_minutes).time()
#             new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
#             new_dictionary["data"].append(new_dictionary_item)
#         config.PrayerTime = new_dictionary
#         config.elfajer, config.duhr, config.alasr, config.almaghreb, config.alaicha = get_todays_prayers().values()
