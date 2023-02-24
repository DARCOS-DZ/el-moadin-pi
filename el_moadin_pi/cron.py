from constance import config
from adan.utils import get_todays_prayers, get_zigbee_state
from adan.tasks import prayer_audio_task
from datetime import datetime, timedelta
from django.conf import settings
from mqtt import mqtt_publisher
import time
import json

PRAYER_TIMES = ["elfajer", "duhr", "alasr", "almaghreb", "alaicha"]
DEADLINE = timedelta(minutes=10)

def daily():
    now = datetime.now()
    prayers = get_todays_prayers()
    print(f"Cronjob: {now}")

    for prayer in PRAYER_TIMES:
        if not getattr(config, f"{prayer}_schedul"):
            prayer_time = datetime.strptime(f"{now.strftime('%Y,%m,%d')} {prayers[prayer]}", "%Y,%m,%d %H:%M:%S")
            prayer_diff = prayer_time - now
            if prayer_diff < timedelta(0):
                pass
            elif prayer_diff < DEADLINE:
                prayer_audio_task(prayer=prayer, schedule=prayer_time)
                setattr(config, f"{prayer}_schedul", True)


def send_plug_state():
    count = 0
    while True:
        if count == 40:
            break
        else :
            try:
                topic = "raspberry_pi/{}".format(settings.SERIAL_NUMBER)
                # Sends an "init" message to the topic with device information.
                json_msg={
                    "operation": "init",
                    "sender": 1,
                    "data": {
                        "model": "Topic",
                        "topic_serial_number": settings.SERIAL_NUMBER,
                        "mosque_name": config.mosque,
                    }
                }
                message = json.dumps(json_msg, ensure_ascii=False)
                mqtt_publisher.main(topic, message)
                print(json_msg)
                # Publishes the current state of the device.
                json_msg={
                    "operation": "transfer",
                    "sender": 1,
                    "data": {
                        "model": "Plug",
                        "state": get_zigbee_state(),
                        "date": str(datetime.now()),
                        "topic_serial_number": settings.SERIAL_NUMBER
                    }
                }
                message = json.dumps(json_msg, ensure_ascii=False)
                mqtt_publisher.main(topic, message)
                print(json_msg)
            except Exception as e:
                print(e)
        count += 1
        time.sleep(1)
