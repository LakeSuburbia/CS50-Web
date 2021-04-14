from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follows(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey('User', on_delete=models.CASCADE, related_name="followee")
    
class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    body = models.TextField(max_length=140)
    time = models.DateTimeField()

class Likes(models.Model):
    liker = models.ForeignKey('User', on_delete=models.CASCADE)
    liked = models.ForeignKey('Post', on_delete=models.CASCADE)
