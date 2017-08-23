from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from adminpanel.models.countriesmodel import *

class States(models.Model):
    name = models.CharField(max_length=255,null=True)
    country = models.ForeignKey(Countries,null=True,blank=True)