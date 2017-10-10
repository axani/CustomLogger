from django.db import models
from django.utils import timezone

# Create your models here.
class LogButton(models.Model):
    name = models.CharField(max_length=200)
    token = models.ForeignKey(
        'tokenizer.Token'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
            return self.name

class LogEntry(models.Model):
    initiating_button = models.ForeignKey(
        'LogButton'
    )
    token = models.ForeignKey(
        'tokenizer.Token'
    )
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
            return self.name