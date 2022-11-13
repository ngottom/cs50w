from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("active", views.activeListings, name="active"),
    path("categories", views.categories, name="categories"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("sortWatchlist", views.sortWatchlist, name="sortWatchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),


]
