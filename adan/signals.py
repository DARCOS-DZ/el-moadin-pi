from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *


@receiver(post_save, sender=LiveEvent)
def message_signal(sender, instance, **kwargs):
    import wget
    from pathlib import Path
    from django.core.files import File
    audio = str(instance.audio)
    try:
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        print(downloaded_file)
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
    except Exception as e:
        pass 
