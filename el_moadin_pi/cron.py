from constance import config
from adan.utils import get_todays_prayers
from adan.tasks import *
from datetime import datetime

def daily():
    # Variables
    now = datetime.now()
    prayers = get_todays_prayers()
    deadline = 600
    print("Cronjob :", now)
    # Setting prayer hours
    config.elfajer = prayers["elfajer"]
    config.duhr = prayers["duhr"]
    config.alasr = prayers["alasr"]
    config.almaghreb = prayers["almaghreb"]
    config.alaicha = prayers["alaicha"]

    if config.elfajer_schedul == False :
        # verify if elfajers deadline have been crossed
        elfajer = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.elfajer), "%Y,%m,%d %H:%M:%S")
        elfajer_dif = elfajer - now
        if elfajer_dif.total_seconds() < 0 :
            pass
        elif elfajer_dif.total_seconds() < deadline :
            prayer_audio_task(prayer="elfajer", schedule=elfajer)
            config.elfajer_schedul = True

    if config.duhr_schedul == False :
        # verify if duhrs deadline have been crossed
        duhr = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.duhr), "%Y,%m,%d %H:%M:%S")
        duhr_dif = duhr - now
        if duhr_dif.total_seconds() < 0 :
            pass
        elif duhr_dif.total_seconds() < deadline :
            prayer_audio_task(prayer="duhr", schedule=duhr)
            config.duhr_schedul = True

    if config.alasr_schedul == False :
        # verify if alasrs deadline have been crossed
        alasr = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.alasr), "%Y,%m,%d %H:%M:%S")
        alasr_dif = alasr - now
        if alasr_dif.total_seconds() < 0 :
            pass
        elif alasr_dif.total_seconds() < deadline :
            prayer_audio_task(prayer="alasr", schedule=alasr)
            config.alasr_schedul = True

    if config.almaghreb_schedul == False :
        # verify if almaghrebs deadline have been crossed
        almaghreb = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.almaghreb), "%Y,%m,%d %H:%M:%S")
        almaghreb_dif = almaghreb - now
        if almaghreb_dif.total_seconds() < 0 :
            pass
        elif almaghreb_dif.total_seconds() < deadline :
            prayer_audio_task(prayer="almaghreb", schedule=almaghreb)
            config.almaghreb_schedul = True

    if config.alaicha_schedul == False :
        # verify if alaichas deadline have been crossed
        alaicha = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.alaicha), "%Y,%m,%d %H:%M:%S")
        alaicha_dif = alaicha - now
        if alaicha_dif.total_seconds() < 0 :
            pass
        elif alaicha_dif.total_seconds() < deadline :
            config.alaicha_schedul = True
            prayer_audio_task(prayer="alaicha", schedule=alaicha)
