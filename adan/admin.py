from django.contrib import admin
from .models import *
# Register your models here.

class PrayerEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'prayer', 'audio', 'audio_duration', 'created_at')

class PostCodesAdmin(admin.ModelAdmin):
    exclude = ('pcname',)  #This exclude function will do which u want!
    list_display = ('id', 'gisid', 'title', )

admin.site.register(PrayerEvent, PrayerEventAdmin)
admin.site.register(LiveEvent)
admin.site.register(PrayerAudio)
