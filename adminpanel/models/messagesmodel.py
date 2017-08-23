from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Messages(models.Model):
    subject = models.CharField(max_length=255,null=True)
    body = models.TextField(null=True)
    thread_id = models.CharField(max_length=200,null=True)
    touser = models.ForeignKey(User, related_name = 'touser', on_delete=models.CASCADE,null=True,blank=True)
    fromuser = models.ForeignKey(User, related_name = 'fromuser', on_delete=models.CASCADE,null=True,blank=True)
    is_deleted_thread = models.CharField(max_length=200,null=True,blank=True,default=0)
    is_deleted_msg = models.CharField(max_length=200,null=True,blank=True,default=0)
    is_new_thread = models.CharField(max_length=200,null=True,blank=True,default=0)
    is_read_to = models.CharField(max_length=200,null=True,blank=True,default=0)
    msg_date = models.DateTimeField(
            default=timezone.now)     