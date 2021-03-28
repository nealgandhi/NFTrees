import json
import datetime
import os
import pytz
import sys
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from .forms import DocumentForm, AuctionForm
from .models import Token, Auction

sys.path.append(os.path.abspath('../accounts'))
from accounts.models import Profile


# Create your views here.
def index(request):
    context = {}

    if request.user.is_authenticated:
        request.user.__class__ = Profile
        minted = json.loads(request.user.minted)
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        minted = None
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})

    if request.method == "GET":
        mint_form = DocumentForm()
    else:
        mint_form = DocumentForm(request.POST, request.FILES)
        if mint_form.is_valid:
            # Save file to /uploads/
            file = request.FILES["file"]
            short_path = default_storage.save(str(file), ContentFile(file.read()))
            full_path = os.path.join(settings.MEDIA_ROOT, short_path)

            # Create new Token
            new_token = Token()
            new_token.title = mint_form.__dict__["data"]["title"]
            new_token.category = mint_form.__dict__["data"]["category"]
            new_token.filepath = full_path
            new_token.owner = request.user.username
            new_token.save()
            minted.append(str(new_token.token))
            request.user.minted = json.dumps(list(set(minted)))
            request.user.save()
    context.update({"form": mint_form})
    if minted:
        context.update({"minted_tokens": minted})
    return render(request, 'mint.html', context)


def auctions(request):
    context = {}
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})
    auctions = []
    for auction in Auction.objects.all():
        print(str(auction.time_start))
        start = datetime.datetime.strptime(str(auction.time_start), "%Y-%m-%d %H:%M:%S.%f%z")
        end = start + datetime.timedelta(days=auction.n_days)
        now = pytz.utc.localize(datetime.datetime.now())
        if end > now:
            auctions.append((f"<a href='auctions/{auction.id.token}'>{auction.id.title}</a>", auction.owner,
                             auction.id.category, (end - now).days, "$" + str(auction.current_price)))
    context.update({"auctions": auctions})
    return render(request, 'auctions/auctions.html', context)


def new_auction(request):
    context = {}
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})

    user = Profile.objects.get(pk=request.user.pk)

    if request.method == "GET":
        form = AuctionForm()
        form.set_token_choice(user)
    else:
        form = AuctionForm(request.POST)
        form.set_token_choice(user)
        t = Token.objects.get(token=request.POST["token"])
        if Auction.objects.filter(id=t).count() == 0 and int(request.POST["n_days"]) > 0:
            new_auction_model = Auction()
            new_auction_model.id = t
            new_auction_model.owner = request.user.username
            new_auction_model.n_days = int(request.POST["n_days"])
            new_auction_model.current_price = float(request.POST["start_price"])
            new_auction_model.save()
        else:
            print("Oh no!")

        return auctions(request)

    minted = json.loads(user.minted)
    options = []
    for m in minted:
        temp_token = Token.objects.get(token=m)
        if Auction.objects.filter(id=temp_token).count() == 0:
            options.append((temp_token.title, m))
    context.update({"options": options})
    return render(request, 'auctions/new_auction.html', context)


def auction_details(request, token):
    context = {}
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})

    queried_token = Token.objects.get(token=uuid.UUID(token))
    queried_auction = Auction.objects.get(id=queried_token)

    if queried_auction.owner == request.user.username:
        context.update({"show_bid": False})
    else:
        context.update({"show_bid": True})

    if request.method == "POST":
        queried_auction.winning = request.user.username
        queried_auction.current_price = int(queried_auction.current_price * 1.2) + 1
        queried_auction.n_bids += 1
        queried_auction.save()

    context.update({"current_price": queried_auction.current_price,
                    "next_price": int(queried_auction.current_price * 1.2) + 1,
                    "winning": queried_auction.winning})
    context.update(queried_token.jsonify())
    return render(request, 'auctions/auction_details.html', context)


def token_details(request, token):
    context = {}
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})
    queried_token = Token.objects.get(token=uuid.UUID(token))
    context.update(queried_token.jsonify())
    return render(request, 'details.html', context)


def preview(request, token):
    queried_token = Token.objects.get(token=uuid.UUID(token))
    context = {"bytes": open(queried_token.filepath, "rb").read()}
    return render(request, 'static.html', context)
