from background_task import background
from django.conf import settings
from .models import *
from constance import config
from .utils import get_zigbee_state , zigbee_switch

@background(schedule=0)
def prayer_event_task(id):
    # lookup user by id and send them a message
    live_event = PrayerEvent.objects.get(id=id)
    import pygame
    absolute_path = str(settings.BASE_DIR) + live_event.audio.url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@background(schedule=0)
def live_event_task(id):
    # lookup user by id and send them a message
    live_event = LiveEvent.objects.get(id=id)
    import pygame
    absolute_path = str(settings.BASE_DIR) + live_event.audio.url
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    sound = pygame.mixer.Sound(absolute_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

@background()
def prayer_audio_task(prayer):
    # lookup user by id and send them a message
    import pygame
    try:
        try:
            state = get_zigbee_state()
            if state == "off" :
                url = f"{config.home_assistant_address}/api/services/switch/turn_on"
        except:
            pass
        prayer_audio = PrayerAudio.objects.filter(prayer=prayer).last()
        absolute_path = str(settings.BASE_DIR) + prayer_audio.audio.url
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        sound = pygame.mixer.Sound(absolute_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
        if prayer == "elfajer" :
            config.elfajer_schedul = False
        elif prayer == "duhr" :
            config.duhr_schedul = False
        elif prayer == "alasr" :
            config.alasr_schedul = False
        elif prayer == "almaghreb" :
            config.almaghreb_schedul = False
        elif prayer == "alaicha" :
            config.alaicha_schedul = False
    except:
        if prayer == "elfajer" :
            absolute_path = str(settings.BASE_DIR) + "/audio/audio_azan.mp3"
        else :
            absolute_path = str(settings.BASE_DIR) + "/audio/audio_azansubuh.mp3"
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        sound = pygame.mixer.Sound(absolute_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
        if prayer == "elfajer" :
            config.elfajer_schedul = False
        elif prayer == "duhr" :
            config.duhr_schedul = False
        elif prayer == "alasr" :
            config.alasr_schedul = False
        elif prayer == "almaghreb" :
            config.almaghreb_schedul = False
        elif prayer == "alaicha" :
            config.alaicha_schedul = False
