from . import mqtt_client

client = mqtt_client.main()
client.loop_start()
