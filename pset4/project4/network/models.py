from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follows(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey('User', on_delete=models.CASCADE, related_name="followee")
    