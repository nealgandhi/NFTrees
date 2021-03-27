from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('auction', views.auction, name="auction"),
    path('accounts/sign_up/', views.sign_up, name="sign-up")
]
