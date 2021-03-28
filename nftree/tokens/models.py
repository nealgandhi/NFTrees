from django.db import models
import sys, os

sys.path.append(os.path.abspath('../accounts'))
from accounts.models import Profile
import uuid
import json


class Token(models.Model):
    CATEGORIES = (("ART", "Art"),
                  ("MUS", "Music"),
                  ("ETC", "Other"))

    title = models.CharField(max_length=255)
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.CharField(max_length=20)
    filepath = models.TextField()
    category = models.CharField(
           max_length=3,
           choices=CATEGORIES
       )
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)

    def jsonify(self):
        readable_category = "ERROR"
        for cat in self.CATEGORIES:
            if self.category == cat[0]:
                readable_category = cat[1]
        return {"title": str(self.title),
                "owner": str(self.owner),
                "category": str(readable_category),
                "uuid": str(self.token),
                "filepath": str(self.filepath),
                "date_posted": str(self.date_posted)}


class Auction(models.Model):
    id = models.ForeignKey(Token, on_delete=models.CASCADE, primary_key=True, unique=True)
    owner = models.CharField(max_length=20)
    n_bids = models.IntegerField(default=0)
    time_start = models.DateTimeField(auto_now_add=True)
    n_days = models.IntegerField()
    current_price = models.IntegerField()


class Bid(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)
