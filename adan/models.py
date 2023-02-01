from django.db import models
import mutagen
from datetime import datetime
PRAYER= (('elfajer','elfajer'),('duhr','duhr'),('alasr','alasr'),('almaghreb','almaghreb'),('alaicha','alaicha'))

class PrayerAudio(models.Model):
    audio = models.FileField(upload_to="prayer_audio")
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    downloaded = models.BooleanField(default=False)
    def __str__(self):
        return self.prayer

class LiveEvent(models.Model):
    """This event is triggered immediately"""
    audio = models.FileField(upload_to="live_event")
    name = models.CharField(max_length=120,null=True)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    downloaded = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

class PrayerEvent(models.Model):
    TYPE = (('after','after'),('before','before'))
    type = models.CharField(max_length=50,choices=TYPE)
    name = models.CharField(max_length=120,null=True)
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio = models.FileField(upload_to="prayer_event", max_length=250,null=True,blank=True)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField()
    downloaded = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.type}-{self.prayer}"
