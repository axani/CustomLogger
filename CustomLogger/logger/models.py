from django.db import models


# Create your models here.
class LogButton(models.Model):
    name = models.CharField(max_length=200)
    token = models.ForeignKey(
        'tokenizer.Token'
    )

    def __str__(self):
            return self.name