from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Bid, Listing, User


def index(request):
    return render(request, "auctions/index.html",
    {
        "listings": Listing.objects.all()
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

def sell(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            seller = request.user
            product = request.POST["product"]
            description = request.POST["description"]
            price = request.POST["price"]
            image = request.POST["image"]
    
            try:
                listing = Listing(seller = seller, product = product, description = description, price = price, image = image)
                listing.save()
            except IntegrityError:
                return render(request, "auctions/sell.html", {
                    "message": "Listing is in conflict with another listing"
                })
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/sell.html")

       
def bid(request, listingid):
    if request.method == "post":
        if request.user.is_authenticated:
            price = request.POST["price"]
            buyer = request.user
            listing = Listing.objects.get(id=listingid)

            try:
                bid = Bid(price = price, buyer = buyer, listing = listing)
                bid.save()
            except IntegrityError:
                return render(request, "auctions/index.html", {
                    "message": "Bid did not work"
                })
            
            return render(request, "auctions/index.html")
        else:
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/index.html")
