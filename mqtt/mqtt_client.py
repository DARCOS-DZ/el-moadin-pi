import paho.mqtt.client as mqtt
import json
from datetime import datetime
from django.conf import settings
from constance import config
from django.utils import timezone
import background
import time
from adan.utils import get_zigbee_state, zigbee_switch
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected to raspberry_pi/{} with result code ".format(settings.SERIAL_NUMBER)+str(rc) + "\n")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    topic = "raspberry_pi/{}".format(settings.SERIAL_NUMBER)
    client.subscribe(topic, qos=1)
    json_msg={
	"operation": "init",
	"sender": 1,
	"data": {
        "model": "Topic",
		"topic_serial_number": settings.SERIAL_NUMBER,
		"mosque_name": config.mosque,
	    }
    }
    try:
        message = json.dumps(json_msg,ensure_ascii=False)
        client.publish(topic, message, qos=1)
        json_msg={
    	"operation": "transfer",
    	"sender": 1,
    	"data": {
            "model": "Plug",
    		"state": get_zigbee_state(),
            "date": str(datetime.now()),
    	    }
        }
        message = json.dumps(json_msg,ensure_ascii=False)
        client.publish(topic, message, qos=1)
        print(json_msg)
    except :
        pass


def on_disconnect(client, userdata, rc):
    client.reconnect()

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    try:
        brut_text = str(msg.payload.decode("utf-8"))
        json_msg = json.loads(brut_text)
        if json_msg["sender"] == 0:
            if json_msg["operation"] == "transfer":
                if json_msg["data"]["model"] == "PrayerAudio":
                    from adan.models import PrayerAudio
                    prayer_audio = PrayerAudio(audio=json_msg["data"]["audio"], prayer=json_msg["data"]["prayer"], audio_duration=json_msg["data"]["audio_duration"])
                    prayer_audio.save()
                    now = datetime.now()
                    print("Prayer audio :", json_msg["data"]["audio"], "recorded for", json_msg["data"]["prayer"], "prayer", "with a duration of", json_msg["data"]["audio_duration"])
                if json_msg["data"]["model"] == "LiveEvent":
                    from adan.models import LiveEvent
                    live_envent = LiveEvent(audio=json_msg["data"]["audio"], audio_duration=json_msg["data"]["audio_duration"])
                    live_envent.save()
                    now = datetime.now()
                    print("Live Event :", live_envent.audio, "with a duration of", live_envent.audio_duration, "has been successfully recorded")
                if json_msg["data"]["model"] == "PrayerEvent":
                    from adan.models import PrayerEvent
                    prayer_event = PrayerEvent(type=json_msg["data"]["type"], prayer=json_msg["data"]["prayer"], audio=json_msg["data"]["audio"], audio_duration=json_msg["data"]["audio_duration"], created_at=datetime(2023, 1, 5, tzinfo=timezone.get_current_timezone()))
                    prayer_event.save()
                    now = datetime.now()
                    print("Prayer Event :", prayer_event.type, prayer_event.prayer, "with audio file =", prayer_event.audio, "with a duration of :", prayer_event.audio_duration, "has been successfully recorded")
                if json_msg["data"]["model"] == "constance":
                    config.offset_time = json_msg["data"]["offset_time"]
                    print("Done")
                if json_msg["data"]["model"] == "Plug":
                    state = json_msg["data"]["state"]
                    zigbee_switch(state)
                    print(f"Plug switched to {state}")
                    json_msg={
                	"operation": "transfer",
                	"sender": 1,
                	"data": {
                        "model": "Plug",
                		"state": get_zigbee_state(),
                        "date": str(datetime.now()),
                	    }
                    }
                    message = json.dumps(json_msg,ensure_ascii=False)
                    client.publish(topic, message, qos=1)
                    print(json_msg)
        else :
          pass
    except Exception as e:
        print(e)

# @background.task
def main():
    client = mqtt.Client(client_id=str(settings.SERIAL_NUMBER), clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(config.broker_ip, port=1883)
    client.loop_start()
    return client


if __name__ == '__main__':
	main()
	sys.exit(0)
