from django.contrib import admin
from auctions.models import User, Category, ActiveListing, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(ActiveListing)
admin.site.register(Bid)
admin.site.register(Comment)
