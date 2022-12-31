import paho.mqtt.client as mqtt
import json
from datetime import datetime
from django.conf import settings
from constance import config

# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected to raspberry_pi/{} with result code ".format(settings.SERIAL_NUMBER)+str(rc) + "\n")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("raspberry_pi/{}".format(settings.SERIAL_NUMBER), qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        brut_text = str(msg.payload.decode("utf-8"))
        json_msg = json.loads(brut_text)
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
                prayer_event = PrayerEvent(type=json_msg["data"]["type"], repeated=json_msg["data"]["repeated"], prayer=json_msg["data"]["prayer"], audio=json_msg["data"]["audio"], audio_duration=json_msg["data"]["audio_duration"])
                prayer_event.save()
                now = datetime.now()
                print("Prayer Event :", prayer_event.type, prayer_event.prayer, "with a repreat status ==", prayer_event.repeated, ", & audio file =", prayer_event.audio, "with a duration of :", prayer_event.audio_duration, "has been successfully recorded")
    except Exception as e:
        print(e)


def main():
    client = mqtt.Client(client_id=str(settings.SERIAL_NUMBER), clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(config.broker_ip, 1883, 60)
    return client

if __name__ == '__main__':
	main()
	sys.exit(0)
