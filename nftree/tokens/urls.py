from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('auctions', views.auctions, name="auctions"),
    path('auctions/new', views.new_auction, name="new_auction"),
    path('auctions/preview/<slug:token>', views.preview, name="index"),
    path('auctions/<slug:token>', views.auction_details, name="auction_details"),
    path('tokens/<slug:token>', views.token_details, name="token_details")
]
