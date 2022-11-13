from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=300)

    def __str__(self):
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    imageURL = models.CharField(max_length=1000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,  blank=True, null=True, related_name="user")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="listingWatchlist")
    purchased = models.ManyToManyField(
        User, blank=True, null=True, related_name="listingPurchased")

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,  blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE,  blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)
    datetime = models.CharField(
        max_length=100, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self):
        return f"{self.author} about {self.listing}: {self.message}"


# class Purchase(models.Model):
#     listing = models.ForeignKey(
#         Listing, on_delete=models.CASCADE,  blank=True, null=True, related_name="listingPurchase")
#     purchaseUser = models.ForeignKey(
#         User, on_delete=models.CASCADE,  blank=True, null=True, related_name="purchaseUser"),
#     purchaseListing = models.ForeignKey(
#         Listing, on_delete=models.CASCADE,  blank=True, null=True, related_name="purchaseListing")
