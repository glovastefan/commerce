from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Category, ActiveListing, Bid, Comment


def index(request):
    return render(
        request,
        "auctions/index.html",
        {"all_listings": ActiveListing.objects.all().order_by("-active")},
    )


@login_required
def listing_page(request, id):
    listing = get_object_or_404(ActiveListing, pk=id)
    try:
        all_comments = Comment.objects.filter(listing_id=listing)
    except:
        all_comments = "No any comments yet!"
    current_user = request.user
    is_seller = current_user == listing.seller
    if listing.current_bid == listing.starting_bid:
        min_bid = listing.starting_bid
    else:
        min_bid = listing.current_bid + 1
    if request.method == "POST":
        listing.active = False
        listing.save()
        return redirect("listing_page", id=listing.id)

    else:
        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "current_user": current_user,
                "is_seller": is_seller,
                "min_bid": min_bid,
                "all_comments": all_comments,
            },
        )


@login_required
def add_to_watchlist(request, id):
    listing = get_object_or_404(ActiveListing, pk=id)
    current_user = request.user
    if request.method == "POST":
        listing.watchlisted.add(current_user)
        return redirect("listing_page", id=listing.id)


@login_required
def remove_from_watchlist(request, id):
    listing = get_object_or_404(ActiveListing, pk=id)
    current_user = request.user
    if request.method == "POST":
        listing.watchlisted.remove(current_user)
        return redirect("listing_page", id=listing.id)


@login_required
def place_bid(request, id):
    listing = get_object_or_404(ActiveListing, pk=id)
    current_user = request.user
    try:
        all_comments = Comment.objects.filter(listing_id=listing)
    except:
        all_comments = "No any comments yet!"
    is_seller = current_user == listing.seller
    if listing.current_bid == listing.starting_bid:
        min_bid = listing.starting_bid
    else:
        min_bid = listing.current_bid + 1
    if request.method == "POST":
        new_bid = float(request.POST["current_user_bids"])
        if new_bid >= min_bid:
            bid_to_add = Bid(
                listing_id=listing, user_id=current_user, bid_value=new_bid
            )
            bid_to_add.save()

            listing.current_bid = new_bid
            listing.current_bid_user = current_user
            listing.save()
        else:
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": listing,
                    "current_user": current_user,
                    "is_seller": is_seller,
                    "min_bid": min_bid,
                    "all_comments": all_comments,
                    "error": f"Your Bid must be minimum {min_bid}!",
                },
            )
    return redirect("listing_page", id=listing.id)


@login_required
def add_comment(request, id):
    listing = get_object_or_404(ActiveListing, pk=id)
    current_user = request.user
    your_comment = request.POST["your_comment"]
    if request.method == "POST":
        if your_comment != "":
            comment_to_add = Comment(
                listing_id=listing, user_id=current_user, detailed_comment=your_comment
            )
            comment_to_add.save()
    return redirect("listing_page", id=listing.id)


@login_required
def users_watchlist(request):
    current_user = request.user
    watchlist = current_user.user_watching.all()
    return render(
        request, "auctions/watchlist.html", {"users_watchlist": watchlist}
    )


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
            current_bid_user=request.user,
        )
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"all_categories": Category.objects.all()},
        )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
