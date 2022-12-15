import paho.mqtt.client as mqtt
from .models import *
import json
from datetime import datetime
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected with result code "+str(rc) + "\n")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

def main():
    client = mqtt.Client(client_id='1', clean_session=False)
    client.on_connect = on_connect
    client.connect("192.168.0.155", 1883, 60)
    # for later in the project
    # paho.mqtt.publish.single(
	# 	topic='[topic]',
	# 	payload='[message]',
	# 	qos=2,
	# 	hostname='[hostname]',
	# 	port=8883,
	# 	client_id='[clientid]',
	# 	auth={
	# 		'username': '[username]',
	# 		'password': '[password]'
	# 	},
	# 	tls={
	# 		'ca_certs': '/etc/ssl/certs/DST_Root_CA_X3.pem',
	# 		'tls_version': ssl.PROTOCOL_TLSv1_2
	# 	}
	# )
    return client

if __name__ == '__main__':
	main()
	sys.exit(0)
