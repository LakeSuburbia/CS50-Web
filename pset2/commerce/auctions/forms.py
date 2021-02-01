from django import forms
from auctions.models import Bid, Comment, Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing

        fields = ["title", "desc", "image", "starting_price"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control ml-2 mr-2", "style": "width: 100%;"}),
            "desc": forms.Textarea(attrs={"class": "form-control ml-2 mr-2", "style": "width: 100%;"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file", "name": "image"}),
            "starting_price": forms.NumberInput(attrs={"class": "form-control mt-4"})
        }
