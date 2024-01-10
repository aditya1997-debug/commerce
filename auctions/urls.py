from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("",  views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:pk>", views.listing, name="listing-detail"),
    path("watchlist_page", views.watchlist_page,name="watchlist_page"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("remove-from-watchlist/<int:pk>", views.removefromwatchlist, name="removelisting"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug>", views.foo, name="foo"),
    path("closeyourlisting/<slug>", views.closeyourlistings, name="closeyourlisting"),
    path("closed", views.closed, name="closed")
]
