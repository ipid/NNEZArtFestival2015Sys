from django.db import models
from datetime import datetime

# Create your models here.

class TicketApplication(models.Model):
    grade = models.CharField(max_length=1,default="0")
    no = models.CharField(max_length = 2,default="0")
    name = models.CharField(max_length = 4)
    schoolID = models.CharField(max_length = 6)
    societyID = models.CharField(max_length = 18)
    requirement = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default = datetime(1,1,1))

