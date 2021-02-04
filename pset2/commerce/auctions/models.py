from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.core.validators import MinValueValidator




class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=CASCADE, related_name="sellers")
    product = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10 ,decimal_places=2, default=0, validators=[MinValueValidator(0)])
    image = models.URLField(default="https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg")
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.seller} is selling {self.product} for a minimum price of {self.price} euro."

class Bid (models.Model):
    price = models.DecimalField(max_digits=10 ,decimal_places=2, default=0, validators=[MinValueValidator(0)])
    buyer = models.ForeignKey(User, on_delete=CASCADE, related_name="buyers")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.buyer} Plaatst een bod op product: {self.listing.product} van {self.price} euro"

    
