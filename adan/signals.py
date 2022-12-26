from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.conf import settings

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
def message_signal(sender, instance, **kwargs):
    import wget
    from pathlib import Path
    from django.core.files import File
    audio = str(instance.audio)
    try:
        from .tasks import prayer_audio_task
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
        date = datetime(year=2022, month=12, day=26, hour=21, minute=51, second=45)
        # print(shecule)
        prayer_audio_task(instance.id, schedule=date)

    except Exception as e:
        pass
