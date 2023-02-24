from constance import config
from adan.utils import get_todays_prayers, get_zigbee_state
from adan.tasks import prayer_audio_task
from datetime import datetime, timedelta
from django.conf import settings
from mqtt import mqtt_publisher
import time
import json

PRAYER_TIMES = ["elfajer", "duhr", "alasr", "almaghreb", "alaicha"]
DEADLINE = 600

def daily():
    now = datetime.now()
    prayers = get_todays_prayers()
    print(f"Cronjob: {now}")

    for prayer in PRAYER_TIMES:
        print(prayer)
        setattr(config, f"{prayer}", prayers[prayer])
        if getattr(config, f"{prayer}_schedul") == False :
            prayer_time = getattr(config, f"{prayer}")
            prayer_time = datetime.strptime(f"{now.strftime('%Y,%m,%d')} {prayer_time}", "%Y,%m,%d %H:%M:%S")
            prayer_diff = prayer_time - now
            if prayer_diff.total_seconds() < 0:
                print("fdsfdsfdsfds")
                pass
            elif prayer_diff.total_seconds() < DEADLINE:
                print(f"{prayer} prayer time is less than 10 minutes away.")
                prayer_audio_task(prayer=prayer, schedule=prayer_time)
                setattr(config, f"{prayer}_schedul", True)


def send_plug_state():
    count = 0
    while count < 40:
        try:
            topic = f"raspberry_pi/{settings.SERIAL_NUMBER}"
            # Sends an "init" message to the topic with device information.
            init_msg = {
                "operation": "init",
                "sender": 1,
                "data": {
                    "model": "Topic",
                    "topic_serial_number": settings.SERIAL_NUMBER,
                    "mosque_name": config.mosque,
                }
            }
            mqtt_publisher.main(topic, json.dumps(init_msg, ensure_ascii=False))
            print(init_msg)

            # Publishes the current state of the device.
            transfer_msg = {
                "operation": "transfer",
                "sender": 1,
                "data": {
                    "model": "Plug",
                    "state": get_zigbee_state(),
                    "date": str(datetime.now()),
                    "topic_serial_number": settings.SERIAL_NUMBER
                }
            }
            mqtt_publisher.main(topic, json.dumps(transfer_msg, ensure_ascii=False))
            print(transfer_msg)

        except Exception as e:
            print(e)

        count += 1
        time.sleep(1)
