from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listingTitle = models.CharField(max_length=64)
    listingCategory = models.CharField(max_length=38)
    listingDesc = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=500)
    listedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    # currentPrice = models.PositiveIntegerField()
    # bidding = models.ForeignKey(Bidding, null=True, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

class Bidding(models.Model):
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    biddingUser = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
