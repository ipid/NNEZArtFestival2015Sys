from django.db import models
import datetime

# Create your models here.

class TicketApplication(models.Model):
    grade = models.CharField(max_length=1, default="1")
    classNo = models.CharField(max_length = 2, default="1")
    name = models.CharField(max_length = 4)
    schoolID = models.CharField(max_length = 6)
    societyID = models.CharField(max_length = 18)
    requirement = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default=datetime.datetime.now())

