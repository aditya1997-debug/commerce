from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from auctions.models import Bid, User, Auction,Comment,Watchlist,CATEGORIES
from auctions.forms import Auctionform, Bidform, Commentform


def index(request):
    active = Auction.objects.filter(closed=False)
    return render(request,"auctions/index.html",{
        "active": active
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
def create(request):
    if request.method == "POST":
        form = Auctionform(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.save()
            messages.add_message(request, messages.SUCCESS, "Listing created successfully")
        return HttpResponseRedirect(reverse("index"))        
    else:        
        form = Auctionform
        return render(request, "auctions/create.html",{
        "forms": form
        })

@login_required
def listing(request, pk):
    try:
        auction = Auction.objects.get(id=pk)
        if Watchlist.objects.filter(user=request.user, item=auction.id).exists():
            added = True
        else:
            added = False    
        winner = Bid.objects.filter(auction=pk)
        if auction.closed == False: 
            highest_bidder = Bid.objects.filter(auction=auction.id).last
            n = auction.price    
            if request.method == "POST":
                if 'bid' in request.POST:
                    bid_form = Bidform(request.POST)
                    if bid_form.is_valid():
                        x = bid_form.cleaned_data['bid']
                        bid_form.instance.auction = auction
                        bid_form.instance.user = request.user
                        if x > n and x > auction.current_bid:
                            Auction.objects.filter(id=pk).update(current_bid=x)
                            bid_form.save()
                            messages.add_message(request, messages.SUCCESS, "Bid placed Successfully")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        else:
                            messages.add_message(request, messages.ERROR, "Bid price should be greater than current price")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                elif 'comment' in request.POST:
                    comment_form = Commentform(request.POST)
                    if comment_form.is_valid():
                        x = comment_form.cleaned_data['comment']
                        if x == "":
                            messages.add_message(request, messages.ERROR, "Looks like you accidently clicked on a 'Comment' button without commenting anything")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        comment_form.instance.auction = auction
                        comment_form.instance.user = request.user
                        comment_form.instance.comment = x
                        comment_form.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:        
                return render(request, "auctions/listing.html", {
                "listing" : auction,
                "bid" : Bidform,
                "comments" : Comment.objects.filter(auction=auction),
                "comment_box" : Commentform,
                "highest_bidder" : highest_bidder,
                "closed" : False,
                "added" : added
            })
        else:
            return render(request, "auctions/listing.html",{
                "listing": auction,
                "closed": True,
                "winner" : winner[len(winner)-1],
                "highest_bid" : winner[len(winner)-1]
            }) 
    except ValueError:
        auction = Auction.objects.get(id=pk)
        title = auction.title
        return HttpResponse(f"<p>{ title }, This listing has been deleted by the Owner</p>") 


@login_required
def watchlist_page(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html",{
            "watchlist" : watchlist
        })
    except:
        return render(request,"auctions/watchlist.html",{
            "empty" : "Your watchlist is empty"
        })    
    

@login_required
def watchlist(request, pk):
        auction = Auction.objects.get(id=pk)
        item = get_object_or_404(Auction, pk=auction.id)
        #if Watchlist.objects.filter(user=request.user, item=auction.id).exists():
        #    messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        #    return HttpResponseRedirect(reverse("index"))
        user_list, created = Watchlist.objects.get_or_create(user=request.user)    
        user_list.item.add(item)
        messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def removefromwatchlist(request, pk):
    auction = Auction.objects.get(id=pk)
    remove_item = Watchlist.objects.get(user=request.user)
    remove_item.item.remove(auction)
    remove_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": CATEGORIES
    })

@login_required
def foo(request, slug):
    c = Auction.objects.filter(category=slug, closed=False)
    return render(request,"auctions/foo.html",{
        "c" : c
    })

@login_required
def closeyourlistings(request, slug):
    active = Auction.objects.get(id=slug)
    active.closed = True
    active.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
def closed(request):
    closed = Auction.objects.filter(closed=True)
    return render(request, "auctions/closed.html",{
        "closed" : closed
    }) 

