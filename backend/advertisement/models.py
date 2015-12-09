from django.db import models
from datetime import datetime

# Create your models here.

class AdvertisementApplication(models.Model):
    ownerName=models.CharField(max_length=20)
    ownerContact=models.CharField(max_length=1000)
    ownerType=models.CharField(max_length=1)
    shopName=models.CharField(max_length=1000)
    adUrl=models.CharField(max_length=1000)
    timestamp=models.DateTimeField(default=datetime.now())
    validated=models.BooleanField(default=False)
    isJoined=models.BooleanField(default=False)

