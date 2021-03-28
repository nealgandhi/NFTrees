import json
import os
import sys
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from .forms import DocumentForm, AuctionForm
from .models import Token

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
    return render(request, 'auctions.html', context)


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
        if form.is_valid:
            print("Hooray!")
        else:
            print("Oh no!")
    context.update({"form": form})
    return render(request, 'new_auction.html', context)


def token_details(request, token):
    context = {}
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})
    queried_token = Token.objects.get(token=uuid.UUID(token))
    context.update(queried_token.jsonify())
    return render(request, 'details.html', context)
