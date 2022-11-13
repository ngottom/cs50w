from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment

import datetime


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "activeListings": activeListings,
        "categories": categories,
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


def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        # Get data from form
        title = request.POST["title"]
        print(title)
        description = request.POST["description"]
        print(description)

        imageURL = request.POST["imageURL"]
        print(imageURL)
        price = request.POST["price"]
        print(price)
        category = request.POST["category"]
        print(category)
        # who is the user
        currentUser = request.user
        # Get all content about particular category
        categoryData = Category.objects.get(categoryName=category)
        # Create new listing
        newListing = Listing(
            title=title,
            description=description,
            imageURL=imageURL,
            price=float(price),
            category=categoryData,
            owner=currentUser
        )

        # Insert object into database
        newListing.save()
        # print(newListing)
        # print(f"my listing{newListing.title}")
        # print(f"my listing{newListing.description}")
        # print(f"my listing{newListing.imageURL}")
        # print(f"my listing{newListing.price}")
        # Redirect to index
        return HttpResponseRedirect(reverse("index"))


def activeListings(request):
    activeListings = Listing.objects.all()
    print(activeListings)
    categories = Category.objects.all()

    return render(request, "auctions/active.html", {
        "activeListings": activeListings,
        "categories": categories,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(
            isActive=True, category=category)
        allCategories = Category.objects.all()
        allListings = Listing.objects.all()
        print(category)
        print(activeListings)
        return render(request, "auctions/index.html", {
            "activeListings": activeListings,
            "categories": allCategories,
            "allListings": allListings,
        })


def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    # print(isListingInWatchlist)
    # print(f"listingData, {listingData}")
    print(f"comments: {comments}")
    return render(request, "auctions/listing.html", {
        "listingData": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments
    })


def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    print(f"watchlist {listingData.watchlist}")


def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    print(listingData.watchlist)


def watchlist(request):
    currentUser = request.user
    categories = Category.objects.all()
    watchlist = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "categories": categories
    })


def sortWatchlist(request):
    if request.method == "POST":
        currentUser = request.user
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        watchlist = currentUser.listingWatchlist.all()
        sortedWatchlist = watchlist.filter(isActive=True, category=category)

        allCategories = Category.objects.all()
        print(f"sortedwatchlist_is{sortedWatchlist}")
        return render(request, "auctions/sortWatchlist.html", {
            "watchlist": watchlist,
            "categories": allCategories,
            "sortedWatchlist": sortedWatchlist
        })


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    createComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message,
    )
    createComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))


# def purchases(request):
#     listingData = Listing.objects.get(pk=id)
#     isPurchased = request.user in listingData.purchased.all()
#     ordered = False
#     return render(request, id, {
#         "ordered": ordered
#     })
