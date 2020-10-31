from django import forms
from .models import Auction, User, Watch, Bit, Comment


class AuctionForm(forms.Form):
    user_id = forms.CharField(max_length=4)
    product_name = forms.CharField(max_length=54)
    img_url = forms.CharField(max_length=200)
    price = forms.FloatField()
    description = forms.CharField(max_length=64)
    winner_id = forms.ImageField()
    category = forms.CharField(max_length=54)

    def save(self):
        user_id = self['user_id'].value()
        new_auction = Auction.objects.create(
            user = User.objects .get(id=user_id),
            img_url=self['img_url'].value(),
            product_name = self['product_name'].value(),
            price = self['price'].value(),
            description = self['description'].value(),
            winner_id = user_id,
            category = self['category'].value(),
        )
        return new_auction

class CommentForm(forms.Form):
    auction= forms.CharField(max_length=4)
    user = forms.CharField(max_length=4)
    text =  forms.CharField(widget=forms.Textarea())

    def save(self):
        user_id = self['user'].value()
        auction_id = self['auction'].value()

        new_comment = Comment.objects.create(
            user = User.objects.get(id=user_id),
            auction = Auction.objects.get(id=auction_id),
            text = self['text'].value(),
        )
        return new_comment


class BidForm(forms.Form):
    user = forms.CharField(max_length=4)
    auction = forms.CharField(max_length=4)
    new_price = forms.FloatField()

    def bid(self):
        user_id = self['user'].value()
        auction_id = self['auction'].value()
        new_price = self['new_price'].value()

        auction = Auction.objects.get(id=auction_id)

        new_bid = Bit.objects.create(
            user=User.objects.get(id=user_id),
            auction=Auction.objects.get(id=auction_id),
            price=float(new_price)
        )
        auction.price = new_price
        auction.save()

        return new_bid


class WatchlistForm(forms.Form):

    user = forms.CharField(max_length=4)
    auction = forms.CharField(max_length=4)


    def save(self):
        user_id = self['user'].value()
        auction_id = self['auction'].value()
        new_wach = Watch.objects.create(
            user = User.objects.get(id= user_id),
            auction = Auction.objects.get(id=auction_id)
        )
        return new_wach

    def dell(self):

        user_id = self['user'].value()
        auction_id = self['auction'].value()

        wach = Watch.objects.get(user = user_id, auction = auction_id)
        wach.delete()