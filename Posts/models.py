from django.db import models
from datetime import datetime
from Users.models import User

# Create your models here.

cur_time = datetime.utcnow().strftime('%m/%d/%Y %I:%M:%S %p')

class Post(models.Model):
  username = models.ForeignKey(User,on_delete=models.CASCADE)
  text = models.CharField(null=True, max_length=100)
  time = models.CharField(max_length=50, default=cur_time)
