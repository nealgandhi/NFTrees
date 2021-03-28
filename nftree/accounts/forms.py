from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = Profile
        fields = ('username',)

