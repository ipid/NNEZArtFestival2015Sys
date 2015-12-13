from django.db import models
from datetime import datetime

# Create your models here.

class AdvertisementApplication(models.Model):
    ownerName=models.CharField(max_length=20)
    ownerContact=models.CharField(max_length=1000)
    ownerType=models.CharField(max_length=1)
    shopName=models.CharField(max_length=1000)
    adPic=models.CharField(max_length=10000000)
    isJoined=models.CharField(max_length=1)
    isValidated=models.CharField(max_length=1)
    timestamp=models.DateTimeField(default=datetime.now())

