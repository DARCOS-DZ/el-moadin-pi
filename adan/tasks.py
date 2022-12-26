from background_task import background
from django.conf import settings
from .models import *

@background(schedule=0)
def live_event_task(id):
    # lookup user by id and send them a message
    import pygame
    live_event = LiveEvent.objects.get(id=id)
    absolute_path = str(settings.BASE_DIR) + live_event.audio.url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@background(schedule=10)
def prayer_audio_task(id):
    # lookup user by id and send them a message
    prayer_audio = PrayerAudio.objects.get(id=id)
    absolute_path = str(settings.BASE_DIR) + prayer_audio.audio.url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@background(schedule=10)
def prayer_event_task(id):
    # lookup user by id and send them a message
    prayer_event = PrayerEvent.objects.get(id=id)
    absolute_path = str(settings.BASE_DIR) + prayer_event.audio.url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
