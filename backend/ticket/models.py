from django.db import models

# Create your models here.

class Organization(models.Model):
    grade = models.PositiveIntegerField()
    no = models.PositiveIntegerField()

class TicketApplication(models.Model):
    name = models.CharField(max_length = 4)
    organization = models.ForeignKey(Organization)
    schoolID = models.CharField(max_length = 6)
    societyID = models.CharField(max_length = 18)
    requirement = models.PositiveIntegerField(default = 1)

