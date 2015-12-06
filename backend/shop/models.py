from django.db import models

# Create your models here.
class PrivilegeKey(models.Model):
    privilegeKey=models.CharField(max_length=8)

class ShopApplication(models.Model):
    ownerName = models.CharField(max_length = 4)
    ownerGrade = models.CharField(max_length = 1)
    ownerClass= models.CharField(max_length = 2)
    ownerContact = models.CharField(max_length = 64)
    shopName = models.CharField(max_length = 32)
    ownerType = models.CharField(max_length = 1)
    electricity = models.CharField(max_length = 1)
    food = models.CharField(max_length = 1)
    nonFood = models.CharField(max_length = 1)
    privilegeKey = models.CharField(max_length = 8)
    timestamp = models.DateTimeField()
