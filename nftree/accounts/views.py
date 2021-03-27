from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, MintForm
from .models import Profile
import json


def index(request):
    if request.method == "GET":
        mint_form = MintForm()
    else:
        mint_form = MintForm(request.POST)
        if mint_form.is_valid:
            request.user.__class__ = Profile
            minted = json.loads(request.user.minted)
            minted.append(mint_form.data["to_mint"])
            request.user.minted = json.dumps(list(set(minted)))
            print(request.user.minted)
            request.user.save()
    if request.user.is_authenticated:
        auth = {"auth_url": "accounts/logout", "auth_text": "Logout"}
    else:
        auth = {"auth_url": "accounts/login", "auth_text": "Login"}
    auth.update({"form": mint_form})
    return render(request, 'mint.html', auth)


def auction(request):
    if request.user.is_authenticated:
        auth = {"auth_url": "accounts/logout", "auth_text": "Logout"}
    else:
        auth = {"auth_url": "accounts/login", "auth_text": "Login"}
    return render(request, 'auction.html', auth)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/index')
    if request.method == "GET":
        return render(request, 'registration/sign_up.html', {'form': SignUpForm()})
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/index')
    else:
        return render(request, 'registration/sign_up.html', {'form': form})
