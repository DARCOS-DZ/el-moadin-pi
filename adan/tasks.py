from background_task import background
from django.conf import settings
from .models import PrayerEvent, LiveEvent, PrayerAudio
from constance import config
from adan.utils import zigbee_switch
import json
from datetime import datetime, timedelta
import threading


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
    setattr(config, f"schedule_{live_event.type}_{live_event.prayer}", False)
    play_audio(live_event.audio.url)

@background(schedule=0)
def live_event_task(id):
    # lookup user by id and send them a message
    live_event = LiveEvent.objects.get(id=id)
    play_audio(live_event.audio.url)

def get_prayer_configs(now):
    prayer_configs = {
        "elfajer": (config.elfajer_schedul,
                    datetime.strptime(f"{now.strftime('%Y,%m,%d')} {config.elfajer}",
                                      "%Y,%m,%d %H:%M:%S")),
        "duhr": (config.duhr_schedul,
                 datetime.strptime(f"{now.strftime('%Y,%m,%d')} {config.duhr}",
                                      "%Y,%m,%d %H:%M:%S")),
        "alasr": (config.alasr_schedul,
                  datetime.strptime(f"{now.strftime('%Y,%m,%d')} {config.alasr}",
                                      "%Y,%m,%d %H:%M:%S")),
        "almaghreb": (config.almaghreb_schedul,
                      datetime.strptime(f"{now.strftime('%Y,%m,%d')} {config.almaghreb}",
                                      "%Y,%m,%d %H:%M:%S")),
        "alaicha": (config.alaicha_schedul,
                    datetime.strptime(f"{now.strftime('%Y,%m,%d')} {config.alaicha}",
                                      "%Y,%m,%d %H:%M:%S"))
    }
    return prayer_configs

# Define a dictionary to store the flag variables for each prayer
executed_flags = {
    "elfajer": False,
    "duhr": False,
    "alasr": False,
    "almaghreb": False,
    "alaicha": False
}


@background()
def prayer_audio_task(prayer):
    global executed_flags
    # Check if the task has already been executed for this prayer
    if executed_flags[prayer]:
        print(f"Task already executed for {prayer}. Skipping...")
        return
    try:
        zigbee_switch(state="on")
    except Exception as e:
        print("Can't turn the zigbee switch on")
    now = datetime.now()
    prayer_configs = get_prayer_configs(now)
    prayer_audio = PrayerAudio.objects.filter(prayer=prayer).last()
    time_diff = prayer_configs[prayer][1] - now

    if prayer_audio:
        play_audio(prayer_audio.audio.url)
        setattr(config, f"{prayer}_schedul", False)
    else:
        print(f"No prayer audio found for {prayer}.")
        audio_url = "/audio/audio_azansubuh.mp3" if prayer == "elfajer" else "/audio/audio_azan.mp3"
        play_audio(audio_url)
        setattr(config, f"{prayer}_schedul", False)
    # Set the flag variable to indicate that the task has been executed for this prayer
    executed_flags[prayer] = True
