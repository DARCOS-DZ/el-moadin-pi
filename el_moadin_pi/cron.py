from constance import config
from adan.utils import get_todays_prayers
from adan.tasks import *

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
    # config.alaicha = "21:33:30"
    config.alaicha = prayers["alaicha"]

    # verify if elfajers deadline have been crossed
    elfajer = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.elfajer), "%Y,%m,%d %H:%M:%S")
    elfajer_dif = elfajer - now
    if elfajer_dif.total_seconds() < 0 :
        pass
    elif elfajer_dif.total_seconds() < deadline and config.elfajer_schedul == False :
        prayer_audio_task(prayer="elfajer", schedule=elfajer)
        config.elfajer_schedul = True

    # verify if duhrs deadline have been crossed
    duhr = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.duhr), "%Y,%m,%d %H:%M:%S")
    duhr_dif = duhr - now
    if duhr_dif.total_seconds() < 0 :
        pass
    elif duhr_dif.total_seconds() < deadline and config.duhr_schedul == False :
        prayer_audio_task(prayer="duhr", schedule=duhr)
        config.duhr_schedul = True

    # verify if alasrs deadline have been crossed
    alasr = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.alasr), "%Y,%m,%d %H:%M:%S")
    alasr_dif = alasr - now
    if alasr_dif.total_seconds() < 0 :
        pass
    elif alasr_dif.total_seconds() < deadline and config.alasr_schedul == False :
        prayer_audio_task(prayer="alasr", schedule=alasr)
        config.alasr_schedul = True

    # verify if almaghrebs deadline have been crossed
    almaghreb = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.almaghreb), "%Y,%m,%d %H:%M:%S")
    almaghreb_dif = almaghreb - now
    if almaghreb_dif.total_seconds() < 0 :
        pass
    elif almaghreb_dif.total_seconds() < deadline and config.almaghreb_schedul == False :
        prayer_audio_task(prayer="almaghreb", schedule=almaghreb)
        config.almaghreb_schedul = True

    # verify if alaichas deadline have been crossed
    alaicha = datetime.strptime("{} {}".format(now.strftime("%Y,%m,%d"), config.alaicha), "%Y,%m,%d %H:%M:%S")
    alaicha_dif = alaicha - now
    if alaicha_dif.total_seconds() < 0 :
        pass
    elif alaicha_dif.total_seconds() < deadline and config.alaicha_schedul == False :
        config.alaicha_schedul = True
        prayer_audio_task(prayer="alaicha", schedule=alaicha)
