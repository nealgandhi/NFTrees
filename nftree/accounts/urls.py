from django.urls import path
from . import views

urlpatterns = [
    path('accounts/sign_up/', views.sign_up, name="sign-up")
]
