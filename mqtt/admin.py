from django.contrib import admin
from .models import *


class JobSettings(admin.ModelAdmin):

    list_display = ('topic', 'chron', 'sender', 'created_on')
    list_filter = ('topic', 'sender')
    model = Job

class TopicsSettings(admin.ModelAdmin):

    list_display = ('name', 'created_on')
    model = Topics

admin.site.register(Topics, TopicsSettings)
admin.site.register(Job, JobSettings)
# Register your models here.
