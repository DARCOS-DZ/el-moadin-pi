from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.conf import settings

@receiver(post_save, sender=LiveEvent)
def message_signal(sender, instance, **kwargs):
    import wget
    from pathlib import Path
    from django.core.files import File
    audio = str(instance.audio)
    try:
        download  = wget.download(audio, out="media")
        downloaded_file = str(download).encode()
        path = Path(downloaded_file.decode("utf-8"))
        with path.open(mode='rb') as f:
            instance.audio = File(f, name=path.name)
            instance.save()
        absolute_path = str(settings.BASE_DIR) + instance.audio.url
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        sound = pygame.mixer.Sound(absolute_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))

    except Exception as e:
        pass
