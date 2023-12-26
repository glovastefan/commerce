from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class ActiveListing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="listing_as_seller"
    )
    active = models.BooleanField(default=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    url_photo = models.URLField(max_length=250, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    current_bid_user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder"
    )
    watchlisted = models.ManyToManyField(User, blank=True, null=True, related_name="user_watching")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(to=ActiveListing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    bid_value = models.DecimalField(max_digits=6, decimal_places=2)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(to=ActiveListing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )
    detailed_comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
