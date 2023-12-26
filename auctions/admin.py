from django.contrib import admin
from auctions.models import User, Categories, ActiveListing, Bid, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(ActiveListing)
admin.site.register(Bid)
admin.site.register(Comment)
