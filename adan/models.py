from django.db import models
import mutagen
from datetime import datetime
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
    name = models.CharField( max_length=120,null=True)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

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
