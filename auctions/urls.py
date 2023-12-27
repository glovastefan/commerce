from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:id>", views.listing_page, name="listing_page"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("users_watchlist", views.users_watchlist, name="users_watchlist"),
]
