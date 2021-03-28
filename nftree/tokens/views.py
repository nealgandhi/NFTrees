from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Token
from .forms import DocumentForm
import os


# Create your views here.
def index(request):
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
            print(new_token.jsonify())
    if request.user.is_authenticated:
        context = {"auth_url": "accounts/logout", "auth_text": "Logout"}
    else:
        context = {"auth_url": "accounts/login", "auth_text": "Login"}
    context.update({"form": mint_form})
    return render(request, 'mint.html', context)
