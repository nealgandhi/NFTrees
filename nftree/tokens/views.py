import json
import os
import sys

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from .forms import DocumentForm
from .models import Token

sys.path.append(os.path.abspath('../accounts'))
from accounts.models import Profile


# Create your views here.
def index(request):
    context = {}
    request.user.__class__ = Profile
    minted = json.loads(request.user.minted)

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
            new_token.title = mint_form["title"]
            new_token.filepath = full_path
            new_token.save()
            minted.append(str(new_token.token))
            request.user.minted = json.dumps(list(set(minted)))
            request.user.save()
    if request.user.is_authenticated:
        context.update({"auth_url": "accounts/logout", "auth_text": "Logout"})
    else:
        context.update({"auth_url": "accounts/login", "auth_text": "Login"})
    context.update({"form": mint_form})
    context.update({"minted_tokens": minted})
    return render(request, 'mint.html', context)
