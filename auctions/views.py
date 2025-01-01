from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages
from decimal import InvalidOperation
from django.contrib.auth.decorators import login_required
from .forms import AuctionListingForm
from .models import User, Comments, Bids, AuctionListings, WatchList


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "lists": AuctionListings.objects.all()
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

@login_required
def create_list(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionListingForm()
    return render(request, "auctions/creatauction.html", {"form": form})

@login_required
def list_view(request, list_id):
    auction = AuctionListings.objects.get(pk=list_id)
    bid_count = Bids.objects.filter(listing=auction).count()
    watch_list = WatchList.objects.filter(listing=auction).filter(user=request.user)
    owner = auction.user == request.user
    highest_bidder = Bids.objects.filter(listing=auction).order_by('-bid').first()
    comments = Comments.objects.filter(listing=auction)
    if highest_bidder:
        highest_bid = highest_bidder.bid
        is_user_won = highest_bidder.user == request.user
        message = "You are the highest bidder." if is_user_won else "You have been outbid."
    else:
        highest_bid = auction.price
        is_user_won = False
        message = "No one has bid yet!"

    return render(request, "auctions/list.html", {
        "auction": auction,
        "highest_bid": highest_bid,
        "message": message,
        "bid_count": bid_count,
        "watch_list": watch_list,
        "owner": owner,
        "is_user_won": is_user_won,
        "comments": comments
    })

@login_required
def place_bid(request, list_id):
    if request.method == "POST":
        try:
            auction = AuctionListings.objects.get(pk=list_id)
            price = Decimal(request.POST["price"])
            if auction.active == False:
                messages.error(request, "This auction has been finished")
                return HttpResponseRedirect(reverse("list_view", kwargs={'list_id': list_id}))
            if auction.price < price:
                Bids.objects.create(
                    bid=price,
                    user=request.user,
                    listing=auction
                )
                auction.price = price
                auction.save()
                messages.success(request, "Your bid has been placed successfully!")
            else:
                messages.error(request, "Your bid must be higher than the current price.")
        except (TypeError, InvalidOperation):
            messages.error(request, "Your bid must be decimal number.")

    return HttpResponseRedirect(reverse("list_view", kwargs={'list_id': list_id}))

@login_required
def add_watch_list(request, list_id):
    if request.method == "POST":
        try:
            listing = AuctionListings.objects.get(pk=list_id)
            watchlist = WatchList(
                user=request.user,
                listing=listing
            )
            watchlist.save()
            return HttpResponseRedirect(reverse("list_view", kwargs={'list_id': list_id}))
        except AuctionListings.DoesNotExist:
            messages.error(request, "Listing not found.")
            return render(request, 'auctions/list.html', {
                "message": "Listing not found."
            })

@login_required
def remove_watch_list(request, list_id):
    if request.method == "POST":
        try:
            listing = AuctionListings.objects.get(pk=list_id)
            watch_list = WatchList.objects.filter(listing=listing, user=request.user)
            watch_list.delete()
            return HttpResponseRedirect(reverse("list_view", kwargs={'list_id': list_id}))
        except AuctionListings.DoesNotExist:
            messages.error(request, "Listing not found.")
            return render(request, 'auctions/list.html', {
                "message": "Listing not found."
            })

@login_required
def view_watch_list(request):
    watchlist_items = WatchList.objects.filter(user=request.user).select_related('listing')
    return render(request, "auctions/index.html", {
        "title": "Watchlist" if watchlist_items.exists() else "You don't have any auction",
        "lists": [item.listing for item in watchlist_items]
    })

@login_required
def finish_auction(request, list_id):
    if request.method == "POST":
        auction = AuctionListings.objects.get(pk=list_id)
        auction.active = False
        auction.save()
        highest_bidder = Bids.objects.filter(listing=auction).order_by('-bid').first()
        if (not highest_bidder):
            messages.success(request, f"The auction '{auction.title}' has ended. It has no winner")
            return HttpResponseRedirect(reverse("index"))
        winner = highest_bidder.user.username

        messages.success(request, f"The auction '{auction.title}' has ended. The winner is {winner}.")

    return HttpResponseRedirect(reverse("index"))


def add_comment(request, list_id):
    if request.method == "POST":
        auction = AuctionListings.objects.get(pk=list_id)
        user = request.user
        comment = request.POST["comment"]
        new_comment = Comments.objects.create(
            user=user,
            comment=comment,
            listing=auction
        )
    return HttpResponseRedirect(reverse("list_view", kwargs={'list_id': list_id}))

def view_category(request):
    categories = AuctionListings.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/category.html", {
        "title": "Category",
        "categories": categories
    })

def view_category_list(request, category):
    lists = AuctionListings.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "title": "Category" if lists.exists() else "You don't have any auction with this category",
        "lists": lists
    })
