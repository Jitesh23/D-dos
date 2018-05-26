
from __future__ import unicode_literals

from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 150)
    password = models.CharField(max_length = 150)
    phone = models.CharField( max_length = 17, unique = True)

class Event(models.Model):
    name = models.CharField(max_length = 150)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    address = models.CharField(max_length = 150)
    image = models.CharField(max_length = 150, blank = True)
    description = models.CharField(max_length = 150)
    latitude = models.CharField(max_length = 150)
    longitude = models.CharField(max_length = 150)
    users = models.ForeignKey(Users)
