from django.db import models
from datetime import datetime

# Create your models here.

cur_time = datetime.utcnow().strftime('%m-%d-%Y %H:%I:%S %p')

class User(models.Model):
    username= models.CharField( max_length=100, unique=True)
    password= models.CharField( max_length=100)
    modified_time= models.CharField( max_length=50, default = cur_time)
    following= models.ManyToManyField("self", related_name='followers',symmetrical=False,blank=True)
    blocked= models.CharField( max_length=100, unique=True)
    token= models.CharField( max_length=100, unique=True)