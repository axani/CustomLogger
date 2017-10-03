from django.db import models

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=24)

    def __str__(self):
            return self.token