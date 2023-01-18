import time
from mqtt import mqtt_client
import background


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
          cpuserial = line[10:26]
    f.close()
    if cpuserial == "0000000000000000" :
      import random
      cpuserial = random.randint(100000,90000000)
      # cpuserial = "0000000000000000"
    return str(cpuserial)

@background.task
def background_loop():
    while True:
        client = mqtt_client.main()
        time.sleep(41)
        client.disconnect()
        client.loop_stop()
