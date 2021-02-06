from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Bid, Listing, User, Watchlist

def highestBid(product):
    AllCurrentBids = Bid.objects.filter(listing=product.id)
    highest = product.price
    for bids in AllCurrentBids:
        highest = max(highest, bids.price)
    product.price = highest
    product.save()

def highestID(product):
    AllCurrentBids = Bid.objects.filter(id=product)
    highest = product.price
    highID = -1
    for bids in AllCurrentBids:
        if highest < bids.price:
            highest = bids.price
            highID = bids.id
    return highID     



def index(request):
    for product in Listing.objects.all():
        highestBid(product)
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

       
def product(request, productid):

    product=Listing.objects.get(id=productid)
    if product:
        highestBid(product)
        return renderProduct(request, productid=productid)
    else:
        return render(request, index.html)
    

def deactivateProduct(request, productid):
    product = Listing.objects.get(id=productid)
    product.active = False
    product.save()
    return renderProduct(request, productid=productid)



def bid(request, productid):
    if request.method == "POST":
        product = Listing.objects.get(id=productid)
        price = request.POST['price']
        buyer = request.user

        bid = Bid(price = price, buyer = buyer, listing = product)
        bid.save()
        highestBid(product)
        product.newOwner = buyer
        product.save()

        return renderProduct(request, productid=productid)


def renderProduct(request, productid):
    product = Listing.objects.get(id=productid)
    watcher = request.user
    watchee = Listing.objects.get(id=productid)
    watchitemUsers = Watchlist.object.filter(watcher = watcher)
    watchitem = watchitemUsers.object.filter(watchee = watchee)
    return render(request, "auctions/product.html",{
        "id": product.id,
        "product": product.product,
        "price": product.price,
        "description": product.description,
        "seller": product.seller,
        "image": product.image,
        "active": product.active,
        "newOwner": product.newOwner,
        "category": product.category,
        "watchid": watchitem.id,
        "watcher": watchitem.watcher,
        "watchee": watchitem.watchee,
        "watchactive": watchitem.active 
        })

def watchlistAdd(request, productid):
    if request.method == "POST":
        if request.user.is_authenticated:
            watcher = request.user
            watchee = Listing.objects.get(id=productid)
            if request.active:
                watchitem = Watchlist(watcher = watcher, watchee = watchee, active = True)
                watchitem.save()

            else:
                watchitemUsers = Watchlist.object.filter(watcher = watcher)
                watchitem = watchitemUsers.object.filter(watchee = watchee)
                watchitem.active = False
                watchitem.save()
    return renderProduct(request, productid=productid)
