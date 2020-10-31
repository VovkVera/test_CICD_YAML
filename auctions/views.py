from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, User, Comment, Watch

from .forms import AuctionForm, WatchlistForm, BidForm, CommentForm


from django.contrib.auth.decorators import login_required

def index(request):
    active_auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "auctions": active_auctions
    })

def categories(request):
    active_auctions = Auction.objects.filter(active=True)
    categories_auctions = []
    for a in active_auctions:
        category = a.category
        categories_auctions.append(category)
    categories = set(categories_auctions)
    print("categories: " + "\033[32m {}\033[0m".format(str(categories)))

    return render(request, "auctions/categories.html",{
        "categories": categories
    })


@login_required
def watchlist(request):
    user_id = 1
    user = User.objects.get(id=user_id)
    watchlist = Watch.objects.filter(user=user)


    # TODO by request.user (может есть и аукцион ид ??)

    auctions = []
    for w in watchlist:
        auction_id = w.auction.id
        auction = Auction.objects.get(id=auction_id)
        auctions.append(auction)

    return render(request, "auctions/watchlist.html",{
        "auctions": auctions,
        "title": "Your Wacthlist"
    })


def category_page(request, category):
    auctions = Auction.objects.filter(active=True, category__icontains = category)
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
        "title": "In this category next items:"
    })

def auction_page(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    wlist = auction.watchs.all()
    count = auction.watchs.count()
    w_id_list = []
    for w in wlist:
        w_id_list.append(w.user.id)
    comments = Comment.objects.filter(auction=auction)

    return render(request, "auctions/auction.html",{
        "auction": auction,
        "count": count,
        "w_id_list": w_id_list,
        "bidform":BidForm(),
        "commentForm":CommentForm(),
        "comments": comments,
    })

@login_required
def leave_comment(request, auction_id):
    comment = CommentForm(request.POST)
    comment.save()
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))

@login_required
def create(request):
    form = AuctionForm()
    return render(request, "auctions/create.html",{"form":form})

@login_required
def add(request):
    auction = AuctionForm(request.POST)
    auction.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def add_to_watchlist(request):
    wach = WatchlistForm(request.POST)
    wach.save()
    auction_id= wach.data['auction']
    # TODO by request.user (может есть и аукцион ид ??)
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))

@login_required
def close_auction(request):
    newbid =  BidForm(request.POST)
    auction_id = newbid.data['auction']
    winner_id = newbid.data['winner_id']
    auction = Auction.objects.get(id=auction_id)

    auction.active = False
    auction.save()

    return HttpResponseRedirect(reverse("auction", args=[auction_id]))

@login_required
def del_from_watchlist(request):
    wach = WatchlistForm(request.POST)
    auction_id= wach.data['auction']

    wach.dell()

    return HttpResponseRedirect(reverse("auction", args=[auction_id]))

@login_required
def bid(request):
    newbid = BidForm(request.POST)
    auction_id = newbid.data['auction']
    auction = Auction.objects.get(id=auction_id)
    current_price = auction.price
    new_price = newbid.data['new_price']

    if float(new_price) > current_price:
        newbid.bid()
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    else:
        return HttpResponseRedirect(reverse("auction", args=[auction_id])+'?lowbid=true')


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
