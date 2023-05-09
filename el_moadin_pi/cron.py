from constance import config
from adan.utils import get_todays_prayers, get_zigbee_state
from adan.tasks import prayer_audio_task
from datetime import datetime, timedelta
from django.conf import settings
from mqtt import mqtt_publisher
import time
import json
import pytz

PRAYER_TIMES = ["elfajer", "duhr", "alasr", "almaghreb", "alaicha"]
DEADLINE = 300
tz = pytz.timezone(settings.TIME_ZONE)

def daily():
    now = datetime.now(tz)
    prayers = get_todays_prayers()
    print(f"Cronjob: {now}")

    for prayer in PRAYER_TIMES:
        print(prayer)
        try:
            # setattr(config, f"{prayer}", prayers[prayer])
            if getattr(config, f"{prayer}_schedul") == False :
                prayer_time = getattr(config, f"{prayer}")
                prayer_time = datetime.strptime(f"{now.strftime('%Y,%m,%d')} {prayer_time}", "%Y,%m,%d %H:%M:%S")
                prayer_time = tz.localize(prayer_time)
                prayer_diff = prayer_time - now
                if prayer_diff.total_seconds() < 0:
                    pass
                else:
                    if prayer_diff.total_seconds() < DEADLINE:
                        print(f"{prayer} prayer time is less than 10 minutes away.")
                        task = prayer_audio_task.apply_async(args=[prayer], eta=prayer_time)
                        setattr(config, f"{prayer}_schedul", True)
        except Exception as e:
            print(e)
