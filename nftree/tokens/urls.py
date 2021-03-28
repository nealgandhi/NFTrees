from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('tokens/<slug:token>', views.token_details, name="token_details")
]
