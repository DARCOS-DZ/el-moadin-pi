from django.conf import settings
from .models import PrayerEvent, LiveEvent, PrayerAudio
from constance import config
from adan.utils import zigbee_switch
import json
from datetime import datetime, timedelta
from celery import shared_task

def play_audio(audio_url):
    import pygame
    absolute_path = str(settings.BASE_DIR) + audio_url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@shared_task(name='adan.tasks.prayer_event_task',
             bind=True,
             acks_late=True,
             autoretry_for=(Exception,),
             max_retries=5,
             retry_backoff=True,
             retry_backoff_max=500,
             retry_jitter=True)
def prayer_event_task(self, id):
    # lookup user by id and send them a message
    live_event = PrayerEvent.objects.get(id=id)
    setattr(config, f"schedule_{live_event.type}_{live_event.prayer}", False)
    play_audio(live_event.audio.url)

@shared_task(name='adan.tasks.live_event_task',
             bind=True,
             acks_late=True,
             autoretry_for=(Exception,),
             max_retries=5,
             retry_backoff=True,
             retry_backoff_max=500,
             retry_jitter=True)
def live_event_task(self, id):
    # lookup user by id and send them a message
    live_event = LiveEvent.objects.get(id=id)
    play_audio(live_event.audio.url)

@shared_task(name='adan.tasks.prayer_audio_task',
             bind=True,
             autoretry_for=(Exception,),
             max_retries=5,
             retry_backoff=True,
             retry_backoff_max=500,
             retry_jitter=True)
def prayer_audio_task(self, prayer):
    prayer_audio = PrayerAudio.objects.filter(prayer=prayer).last()
    if prayer_audio:
        play_audio(prayer_audio.audio.url)
        setattr(config, f"{prayer}_schedul", False)
    else:
        print(f"No prayer audio found for {prayer}.")
        audio_url = "/audio/audio_azansubuh.mp3" if prayer == "elfajer" else "/audio/audio_azan.mp3"
        play_audio(audio_url)
        setattr(config, f"{prayer}_schedul", False)
