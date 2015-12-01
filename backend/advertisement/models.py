from django.db import models

# Create your models here.

class AdvertisementApplication(models.Model):
    ownerName=models.CharField(max_length=20)
    ownerContact=models.CharField(max_length=1000)
    ownerType=models.CharField(max_length=1)
    shopName=models.CharField(max_length=1000)
    adUrl=models.CharField(max_length=1000)
    isJoined=models.CharField(max_length=1)

