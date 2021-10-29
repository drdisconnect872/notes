from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


def create_hash():
    return str(uuid.uuid4().hex)[:10]


class Message(models.Model):
    hash_key = models.CharField(max_length=10,default=create_hash,unique=True)
    message = models.TextField(max_length=10000)
    time_created = models.DateTimeField(default=timezone.now)
    time_viewed = models.DateTimeField(default=timezone.now)
    destroy_hours = models.IntegerField(default=0)
    destroy_days = models.IntegerField(default=30)
    hidden = models.BooleanField(default=True)
    viewed = models.BooleanField(default=False)
