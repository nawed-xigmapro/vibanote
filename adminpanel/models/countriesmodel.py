from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Countries(models.Model):
    sortname = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    phonecode = models.CharField(max_length=100,null=True)