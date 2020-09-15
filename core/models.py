from django.db import models

# Create your models here.

# 추상모델
class TimeStampedModel(models.Model):
    """ Time Stamped Definition """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
