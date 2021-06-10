from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


def default_start_time():
    now = datetime.now()
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)


class User(AbstractUser):
    pass


class Follows(models.Model):
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="follower"
    )
    followee = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="followee"
    )


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)


class Likes(models.Model):
    liker = models.ForeignKey("User", on_delete=models.CASCADE)
    liked = models.ForeignKey("Post", on_delete=models.CASCADE)
