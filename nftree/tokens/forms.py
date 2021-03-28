from django import forms
import datetime
import json


class DocumentForm(forms.Form):
    CATEGORIES = (("ART", "Art"),
                  ("MUS", "Music"),
                  ("ETC", "Other"))
    title = forms.CharField(max_length=255)
    category = forms.ChoiceField(
        choices=CATEGORIES
    )
    file = forms.FileField(label='Select a file')


class AuctionForm(forms.Form):
    USER_TOKENS = ((1, "Null"),
                   (2, "Null"))
    token = forms.ChoiceField(choices=USER_TOKENS, label="Which token would you like to auction?")
    start_price = forms.FloatField(min_value=1.0, label="Start Price")
    n_days = forms.IntegerField(min_value=1, label="How many days would you like the auction to stay open?")

    def set_token_choice(self, user):
        minted = json.loads(user.minted)
        self.USER_TOKENS = list(enumerate(minted))
        self.token = forms.ChoiceField(choices=self.USER_TOKENS, label="Which token would you like to auction?")

    def clean_end_date(self):
        date = self.__dict__["data"]["end_date"]
        if date < datetime.datetime.now():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
