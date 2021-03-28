from django.urls import path
from . import views

urlpatterns = [
    path('auction', views.auction, name="auction"),
    path('accounts/sign_up/', views.sign_up, name="sign-up")
]
