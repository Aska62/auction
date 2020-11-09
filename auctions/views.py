from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bidding, Comment, Watchlist

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    # else:
    #     if request.method == "POST":
    #         selectedCategory = request.POST["category"]
    #         listingByCategory = Listing.objects.filter(listingCategory=selectedCategory)
    #         selectedBidding = Bidding.objects.filter(listing=listingByCategory)
    #         return render(request, "auctions/index.html", {
    #             "listings": listingByCategory,
    #             "biddings": selectedBidding
    #         })
    else:
        listing = Listing.objects.all
        bidding = Bidding.objects.all
        return render(request, "auctions/index.html", {
            "listings": listing,
            "biddings": bidding
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

# Create new listing
def add_listing(request):
    if request.method == "POST":
        # Get user info from user table
        listedUser = User.objects.get(id=request.POST["listUser"])
        # Set new listing
        newListing = Listing(
            listingTitle = request.POST["title"],
            listingCategory = request.POST["category"],
            listingDesc = request.POST["description"],
            imageUrl = request.POST["image"],
            listedUser = listedUser
        )

        # attempt to add new listing
        try:
            newListing.save()
        except IntegrityError:
            return render(request, "auctions/add-listing.html", {
                "message": "Incorrect input."
            })

        # Set new Bidding
        newlyAddedListing = Listing.objects.get(listingTitle = request.POST["title"])
        newBid = Bidding(
            listing = newlyAddedListing,
            price = request.POST["bidding"],
            biddingUser = listedUser
        )

        # attempt to add new listing and bidding
        try:
            newBid.save()
        except IntegrityError:
            return render(request, "auctions/add-listing.html", {
                "message": "Incorrect input."
            })

        return HttpResponseRedirect(reverse("index"))
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse(login_view))
        else:
            return render(request, "auctions/add-listing.html")

# Show each listing
def show_listing(request, listing_title):
    if request.method == "POST":

        # Get listing info and user info
        shownListing = Listing.objects.get(listingTitle=listing_title)
        updatedUser = User.objects.get(id=request.POST["updatedUser"])

        # Check if the user is listed user
        if updatedUser != shownListing.listedUser:
            # Check if the user has the listing in his watchlist
            existingWatchlist = Watchlist.objects.filter(user=updatedUser)
            exists = False
            for list in existingWatchlist:
                if list.listing == shownListing:
                    exists = True
            # Remove from watchlist if exists already. Add if not
            if exists:
                existingWatchlist.filter(listing=shownListing).delete()
            else:
                newWatchlist = Watchlist(
                    user = updatedUser,
                    listing = shownListing
                )
                newWatchlist.save()
        # If the listed user closes the bid, update db.
        else:
            shownListing.closed = True
            shownListing.save()

        # Return to the listing page after update
        bidding = Bidding.objects.get(listing=shownListing)
        comments = Comment.objects.filter(listing=shownListing)
        watchlist = Watchlist.objects.filter(listing=shownListing)
        return render(request, "auctions/show-listing.html", {
            "listing": shownListing,
            "bidding": bidding,
            "comments": comments,
            "watchlist": watchlist
        })

    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse(login_view))
        else:
            listing = Listing.objects.get(listingTitle=listing_title)
            bidding = Bidding.objects.get(listing=listing)
            comments = Comment.objects.filter(listing=listing)
            watchlist = Watchlist.objects.filter(listing=listing)
            return render(request, "auctions/show-listing.html", {
                "listing": listing,
                "bidding": bidding,
                "comments": comments,
                "watchist": watchlist
            })

# Bid
def bid(request, listing_title):
    if request.method == "POST":
        # Get listing and user info
        shownListing = Listing.objects.get(listingTitle=listing_title)
        updatedUser = User.objects.get(id=request.POST["updatedUser"])

        # Get price from db and user input
        currentBid = Bidding.objects.get(listing=shownListing)
        newPrice = request.POST["bidding-price"]

        # Check if the input is valid.
        if newPrice.isnumeric() == False:
            return render(request, "auctions/show-listing.html", {
                "listing": shownListing,
                "bidding": Bidding.objects.get(listing=shownListing),
                "message": "Enter price in valid number."
            })
        elif float(newPrice) <= float(currentBid.price):
            return render(request, "auctions/show-listing.html", {
                "listing": shownListing,
                "bidding": Bidding.objects.get(listing=shownListing),
                "message": "New price must be higher than current price."
            })

        # Update if valid.
        else:
            currentBid.biddingUser = updatedUser
            currentBid.price = newPrice
            currentBid.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse(login_view))
        else:
            listing = Listing.objects.get(listingTitle=listing_title)
            bidding = Bidding.objects.get(listing=listing)
            comments = Comment.objects.filter(listing=listing)
            return render(request, "auctions/bid.html", {
                "listing": listing,
                "bidding": bidding,
                "comments": comments
            })


# Add Comment
def comment(request, listing_title):
    if request.method == "POST":
        # Get user info from user table
        commentUser = User.objects.get(id=request.POST["commented-user"])
        # Get listing info from listing table
        commentListing = Listing.objects.get(listingTitle=listing_title)

        # Set new comment
        newComment = Comment(
            comment = request.POST["comment-text"],
            user = commentUser,
            listing = commentListing
        )

        # Save if it's valid
        try:
            newComment.save()
        except IntegrityError:
            return render(request, "auctions/coment.html", {
                "message": "Cannot submit the comment."
            })

        listing = Listing.objects.get(listingTitle=listing_title)
        bidding = Bidding.objects.get(listing=listing)
        comments = Comment.objects.filter(listing=listing)
        return render(request, "auctions/show-listing.html", {
            "listing": listing,
            "bidding": bidding,
            "comments": comments
        })
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse(login_view))
        else:
            return render(request, "auctions/comment.html", {
                "listing": Listing.objects.get(listingTitle=listing_title)
            })

# Show watchlist
def watchlist(request):
    return render(request, "auctions/watchlist.html")
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    else:
        watchlist = Watchlist.objects.all
        listings = Listing.objects.all
        biddings = Bidding.objects.all
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
            "biddings": biddings,
            "watchlist": watchlist
        })
