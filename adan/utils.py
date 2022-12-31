from constance import config
from datetime import datetime

def get_todays_prayers():
    current_date_mounth = datetime.today().month
    current_date_day = datetime.today().day
    id_day = (current_date_mounth-1)*30+current_date_day # get current day id
    prayers = config.PrayerTime["data"][id_day]
    return prayers
