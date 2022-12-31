from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.conf import settings
from constance.signals import config_updated
from datetime import datetime, timedelta
from django.utils import timezone

@receiver(post_save, sender=LiveEvent)
def live_event_signal(sender, instance, **kwargs):
    import wget
    from pathlib import Path
    from django.core.files import File
    audio = str(instance.audio)
    try:
        from .tasks import live_event_task, prayer_audio_task
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
    import wget
    from pathlib import Path
    from django.core.files import File
    audio = str(instance.audio)
    try:
        from .tasks import prayer_audio_task
        from .utils import get_todays_prayers
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
        # Calcule adan day
        # current_date_mounth = datetime.today().month
        # current_date_day = datetime.today().day
        # prayers = get_todays_prayers()
        # prayer = prayers[instance.prayer]
        # adan_time = datetime.strptime(prayer, '%H:%M:%S').time()
        # print("Todays Prayer time :", prayer)
        # schedule_adan = datetime(year=2022, month=current_date_mounth, day=current_date_day, hour=adan_time.hour, minute=adan_time.minute, second=adan_time.second)
        # prayer_audio_task(instance.id, schedule=schedule_adan)

    except Exception as e:
        pass

@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    print(sender, key, old_value, new_value)
    if key == "offset_time":
        from constance import config
        from .utils import get_todays_prayers
        prayer_source=json.loads(config.PRAYER_SOURCE)["data"]
        new_dictionary = {"data":[]}
        for prayer in prayer_source :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M %p')+timedelta(minutes=config.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary["data"].append(new_dictionary_item)
        prayers = get_todays_prayers()
        config.PrayerTime = new_dictionary
        config.elfajer = prayers["elfajer"]
        config.duhr = prayers["duhr"]
        config.alasr = prayers["alasr"]
        config.almaghreb = prayers["almaghreb"]
        config.alaicha = prayers["alaicha"]
