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
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filepath = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)

    def jsonify(self):
        payload = {"title": str(self.title),
                   "uuid": str(self.uuid),
                   "filepath": str(self.filepath),
                   "date_posted": str(self.date_posted)}
        return json.dumps(payload)


class Auction(models.Model):
    id = models.ForeignKey(Token, on_delete=models.CASCADE, primary_key=True)
    n_bids = models.IntegerField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()


class Bid(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
