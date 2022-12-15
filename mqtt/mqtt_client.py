import paho.mqtt.client as mqtt
import json
from datetime import datetime
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected with result code "+str(rc) + "\n")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    from .models import Topics, Job
    if Topics.objects.filter(name=msg.topic):
        topic = Topics.objects.get(name=msg.topic)
    else:
        topic_creation = Topics(name=msg.topic)
        topic_creation.save()
        topic = Topics.objects.get(name=topic_creation)

    try:
        brut_text = str(msg.payload.decode("utf-8"))
        json_convert = json.loads(brut_text)
        if json_convert["sender"] == 1:
            message = Job(topic=topic, chron=json_convert["chron"], sender=json_convert["sender"], audio=json_convert["audio"])
            message.save()
            now = datetime.now()
            print(now, "\nFrom Topic: {} \nAudio file path: {} \nIs scheduled for: {} \npublished by: {}".format(topic, json_convert["audio"], json_convert["chron"], json_convert["sender"]))
        else:
          pass
    except Exception as e:
        print("Invalid Json format")
        print(e)

def on_disconnect(client, userdata, rc):
    client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")

def main():
    client = mqtt.Client(client_id='1', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect_async("51.195.148.231", 1883, 60)
    return client

if __name__ == '__main__':
	main()
	sys.exit(0)
