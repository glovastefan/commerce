from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    CAT = (
        ("F", "Fasion"),
        ("T", "Toys"),
        ("O", "Others"),
    )
    category_name = models.CharField(max_length=50, choices=CAT)


class ActiveListing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="listing_as_seller")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    url_photo = models.URLField(max_length=250, blank=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid_user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    watchlisted = models.ManyToManyField(User, blank=True, related_name="user_watching")


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(to=ActiveListing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="bids")
    bid_value = models.DecimalField(max_digits=6, decimal_places=2)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(to=ActiveListing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    detailed_comment = models.TextField(max_length=250)
