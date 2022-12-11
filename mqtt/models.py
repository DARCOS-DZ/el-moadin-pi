from django.db import models
# Create your models here.

sender = (
    (0,"Application"),
    (1,"Controller")
)

class Topics(models.Model):
    name = models.CharField(max_length=150, verbose_name = "Nom", unique=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name = "Date de création")
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
    def __str__(self):
        return self.name


class Job(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    chron = models.CharField(max_length=150, verbose_name = "Chron schedule")
    audio = models.CharField(max_length=150, verbose_name = "Audio path")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name = "Date de création")
    sender = models.IntegerField(choices=sender, default=0, null=True)
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
    def __str__(self):
        return self.audio
