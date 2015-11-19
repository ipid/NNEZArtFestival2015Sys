from django.db import models

# Create your models here.

class Organization(models.Model):
    grade = models.PositiveIntegerField()
    no = models.PositiveIntegerField()

class ShopApplication:
    owner = models.CharField(max_length = 4)
    ownerContact = models.CharField(max_length = 64)
    shopName = models.CharField(max_length = 32)
    ownerType = models.PositiveIntegerField(default = 0)
    ownerOrganization = models.ForeignKey(Organization)
    electricity = models.BooleanField(default = False)
    food = models.BooleanField(default = False)
    nonFood = models.BooleanField(default = False)
    privilegeKey = models.CharField(max_length = 8)
