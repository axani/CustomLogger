from django.db import models
from django.conf import settings

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=24)
    timezone = models.CharField(max_length=40, default=settings.TIME_ZONE)

    def __str__(self):
            return self.token