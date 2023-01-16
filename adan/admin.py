from django.contrib import admin
from .models import *
# Register your models here.

class PrayerEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'prayer', 'audio', 'audio_duration', 'created_at')

admin.site.register(PrayerEvent, PrayerEventAdmin)
