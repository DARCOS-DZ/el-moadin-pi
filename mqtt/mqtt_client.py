def background_loop():
    import paho.mqtt.client as mqtt
    import json
    from datetime import datetime
    from django.conf import settings
    from constance import config
    from django.utils import timezone
    import time
    from adan.utils import get_zigbee_state, zigbee_switch
    import os

    def on_connect(client, userdata, flags, rc):
        """
        Callback function called when the client connects to the MQTT broker.

        Subscribes to the topic for the device with the specified serial number.
        Sends an initial "init" message to the topic with device information.
        Publishes the current state of the device.
        """
        topic = "raspberry_pi/{}".format(settings.SERIAL_NUMBER)
        client.subscribe(topic, qos=1)
        print("connected to:", topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        try:
            # Decode the payload and load it as a JSON object
            brut_text = str(msg.payload.decode("utf-8"))
            json_msg = json.loads(brut_text)

            # Check if the message is sent by the correct sender
            if json_msg["sender"] == 0:
                # Handle different models
                if json_msg["data"]["model"] == "PrayerAudio":
                    # Import the PrayerAudio model
                    from adan.models import PrayerAudio
                    # Create a new instance of PrayerAudio and save it
                    prayer_audio = PrayerAudio(audio=json_msg["data"]["audio"], prayer=json_msg["data"]["prayer"], audio_duration=json_msg["data"]["audio_duration"])
                    prayer_audio.save()
                    # Print a success message
                    print("Prayer audio:", json_msg["data"]["audio"], "recorded for", json_msg["data"]["prayer"], "prayer with a duration of", json_msg["data"]["audio_duration"])
                elif json_msg["data"]["model"] == "LiveEvent":
                    # Import the LiveEvent model
                    from adan.models import LiveEvent
                    # Create a new instance of LiveEvent and save it
                    live_event = LiveEvent(audio=json_msg["data"]["audio"], audio_duration=json_msg["data"]["audio_duration"])
                    live_event.save()
                    # Print a success message
                    print("Live Event:", live_event.audio, "with a duration of", live_event.audio_duration, "has been successfully recorded")
                elif json_msg["data"]["model"] == "PrayerEvent":
                    # Import the PrayerEvent model
                    from adan.models import PrayerEvent
                    # Create a new instance of PrayerEvent and save it
                    prayer_event = PrayerEvent(type=json_msg["data"]["type"], prayer=json_msg["data"]["prayer"], audio=json_msg["data"]["audio"], audio_duration=json_msg["data"]["audio_duration"], created_at=datetime(2023, 1, 5, tzinfo=timezone.get_current_timezone()))
                    prayer_event.save()
                    # Print a success message
                    print("Prayer Event:", prayer_event.type, prayer_event.prayer, "with audio file =", prayer_event.audio, "with a duration of:", prayer_event.audio_duration, "has been successfully recorded")
                elif json_msg["data"]["model"] == "constance":
                    # Set the offset time
                    config.offset_time = json_msg["data"]["offset_time"]
                    # Print a success message
                    print("Offset time set to:", json_msg["data"]["offset_time"])
                elif json_msg["data"]["model"] == "Plug":
                    # Toggle the state of the plug using Zigbee
                    state = json_msg["data"]["state"]
                    zigbee_switch(state)
                    # Print a success message
                    print(f"Plug switched to {state}")
                    # Send a message back to the server with the new state
                    json_msg={
                        "operation": "transfer",
                        "sender": 1,
                        "data": {
                            "model": "Plug",
                            "state": get_zigbee_state(),
                            "date": str(datetime.now()),
                        }
                    }
                    topic = "raspberry_pi/{}".format(settings.SERIAL_NUMBER)
                    message = json.dumps(json_msg,ensure_ascii=False)
                    client.publish(topic, message, qos=1)
                    # Print the sent message
                    print(json_msg)
        except Exception as e:
            # Print the error message
            print("Error occurred while processing the message")

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected from MQTT broker with result code {rc}")
        time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
        client.reconnect()

    while True:
        client = mqtt.Client(client_id=str(settings.SERIAL_NUMBER), clean_session=True)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.connect(config.broker_ip, port=1883)
        client.loop_forever()

if __name__ == '__main__':
    background_loop()
