from background_task import background
from django.conf import settings
from .models import PrayerEvent, LiveEvent, PrayerAudio
from constance import config
from adan.utils import zigbee_switch
import json

def play_audio(audio_url):
    import pygame
    absolute_path = str(settings.BASE_DIR) + audio_url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@background(schedule=0)
def prayer_event_task(id):
    # lookup user by id and send them a message
    live_event = PrayerEvent.objects.get(id=id)
    play_audio(live_event.audio.url)

@background(schedule=0)
def live_event_task(id):
    # lookup user by id and send them a message
    live_event = LiveEvent.objects.get(id=id)
    play_audio(live_event.audio.url)

# Optimization
# Use a dictionary to store the prayer names and config values
schedul_configs = {
    "elfajer": config.elfajer_schedul,
    "duhr": config.duhr_schedul,
    "alasr": config.alasr_schedul,
    "almaghreb": config.almaghreb_schedul,
    "alaicha": config.alaicha_schedul
}

@background()
def prayer_audio_task(prayer):
    # lookup user by id and send them a message
    try:
        zigbee_switch(state="on")
        prayer_audio = PrayerAudio.objects.filter(prayer=prayer).last()
        play_audio(prayer_audio.audio.url)
    except:
        if prayer == "elfajer" :
            audio_url = "/audio/audio_azansubuh.mp3"
        else :
            audio_url = "/audio/audio_azan.mp3"
        play_audio(audio_url)
    schedul_configs[prayer] = False
