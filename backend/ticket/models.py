from django.db import models
from datetime import datetime

# Create your models here.

class TicketApplication(models.Model):
    grade = models.CharField(max_length=1,default="0")
    classNo = models.CharField(max_length = 2,default="0")
    name = models.CharField(max_length = 4,default="0")
    schoolID = models.CharField(max_length = 6,default="0")
    societyID = models.CharField(max_length = 18,default="0")
    requirement = models.CharField(max_length=32,default="0")
    timestamp = models.DateTimeField(default = datetime(1,1,1))

