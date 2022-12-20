

from django.db import models
import json
import mutagen
from constance import config
from datetime import datetime, timedelta
PRAYER= (('elfajer','elfajer'),('duhr','duhr'),('alasr','alasr'),('almaghreb','almaghreb'),('alaicha','alaicha'))

class PrayerAudio(models.Model):
    audio = models.FileField("audio file")
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(PrayerAudio, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return self.prayer

class LiveEvent(models.Model):
    """This event is triggered immediately"""
    audio = models.FileField("audio file")
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(LiveEvent, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return self.id

class State(models.Model):
    name = models.CharField("state name", max_length=120)
    offset_time = models.IntegerField()
    def __str__(self):
        return self.name

class Prayer(models.Model):
    """ Prayer (salat) ``model`` """
    state = models.ForeignKey("adan.state", on_delete=models.CASCADE)
    prayer_time = models.JSONField("prayer data time",null=True,blank=True)
    def __str__(self):
        return self.state.name
    def save(self, *args, **kwargs):
       if self.prayer_time is None or self.prayer_time=="":
        prayer_source=json.loads(config.PRAYER_SOURCE)["data"]
        new_dictionary = {"data":[]}
        for prayer in prayer_source :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary["data"].append(new_dictionary_item)
            self.prayer_time=new_dictionary
            print(alasr)
       super(Prayer, self).save(*args, **kwargs) # Call the real save() method

class PrayerEvent(models.Model):
    TYPE = (('after','after'),('before','before'))
    type = models.CharField(max_length=50,choices=TYPE)
    repeated = models.BooleanField(default=True)
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio = models.FileField(upload_to="prayer_event", max_length=250,null=True,blank=True)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(PrayerEvent, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return f"{self.type}-{self.prayer}"
