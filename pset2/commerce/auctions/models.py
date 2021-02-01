from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateField
import datetime


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.CharField(max_length=256)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    def __str__(self):
        return f"{self.user} placed a listing called {self.title} with a starting price of {self.price} euro."

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")


    def __str__(self):
        return f"{self.user} placed a bet of {self.price} euro."
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True, blank=True)



