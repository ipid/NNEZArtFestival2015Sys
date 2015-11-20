from django.db import models

# Create your models here.

class ShopApplication(models.Model):
    owner = models.CharField(max_length = 4)
    ownerGrade = models.PositiveIntegerField()
    ownerClass = models.PositiveIntegerField()
    ownerContact = models.CharField(max_length = 64)
    shopName = models.CharField(max_length = 32)
    ownerType = models.PositiveIntegerField(default = 0)
    electricity = models.BooleanField(default = False)
    food = models.BooleanField(default = False)
    nonFood = models.BooleanField(default = False)
    privilegeKey = models.CharField(max_length = 8)
    timestamp = models.DateTimeField()
