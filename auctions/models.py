from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.title

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="watchlist_listing")

class Bids(models.Model):
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.bid} on {self.listing.title} by {self.user.username}"

class Comments(models.Model):
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
