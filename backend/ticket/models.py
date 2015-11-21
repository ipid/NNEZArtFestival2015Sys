from django.db import models
from datetime import datetime

# Create your models here.

class TicketApplication(models.Model):
    grade = models.PositiveIntegerField(default = 0)
    no = models.PositiveIntegerField(default = 0)
    name = models.CharField(max_length = 4)
    schoolID = models.CharField(max_length = 6)
    societyID = models.CharField(max_length = 18)
    requirement = models.PositiveIntegerField(default = 1)
    timestamp = models.DateTimeField(default = datetime(1,1,1))

