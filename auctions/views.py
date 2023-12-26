from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, ActiveListing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings": ActiveListing.objects.all()
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        seller = request.user
        try:
            category_id = request.POST["category"]
            category = get_object_or_404(Category, pk=category_id)
        except:
            category = None
        title = request.POST["title"]
        description = request.POST["description"]
        url_photo = request.POST["url_photo"]
        starting_bid = request.POST["starting_bid"]
        ActiveListing.objects.create(
            seller=seller,
            active=True,
            category=category,
            title=title,
            description=description,
            url_photo=url_photo,
            starting_bid=starting_bid,
            current_bid=starting_bid,
            current_bid_user=request.user
        )
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html", {
            "all_categories": Category.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
