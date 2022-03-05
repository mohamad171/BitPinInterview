from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg,Sum

class Post(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)



class Rate(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="rates")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rate_number = models.IntegerField()

