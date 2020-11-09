from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add"),
    path("<str:listing_title>", views.show_listing, name="showListing"),
    path("<str:listing_title>/comment", views.comment, name="comment"),
    path("<str:listing_title>/bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist")
]
