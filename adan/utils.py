from constance import config
from datetime import datetime
import requests
import json

def get_todays_prayers():
    current_date_mounth = datetime.today().month
    current_date_day = datetime.today().day
    id_day = (current_date_mounth-1)*30+current_date_day # get current day id
    prayers = config.PrayerTime["data"][id_day]
    return prayers

def get_zigbee_state():
    url = f"{config.home_assistant_address}/api/states/{config.entity_id}"
    payload={}
    headers = {
      'Authorization': f'Bearer {config.home_assistant_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    object = response.json()
    return object["state"]

def zigbee_switch(state=""):
    if state == "on" :
        url = f"{config.home_assistant_address}/api/services/switch/turn_on"
    elif state == "off" :
        url = f"{config.home_assistant_address}/api/services/switch/turn_off"
    else :
      state = get_zigbee_state()
      if state == "on" :
          url = f"{config.home_assistant_address}/api/services/switch/turn_off"
      elif state == "off" :
          url = f"{config.home_assistant_address}/api/services/switch/turn_on"

    payload = json.dumps({
      "entity_id": config.entity_id
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {config.home_assistant_token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
