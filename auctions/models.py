from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractUser):
    pass

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    category = models.CharField(max_length=54)
    product_name = models.CharField(max_length=54)
    img_url = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField(default='')
    active = models.BooleanField(default=True)
    winner_id = models.IntegerField()


    def __str__(self):
        return f"{self.product_name} ($ {self.price})"

class AuctionManager(models.Manager):
    def create_auction(self, name, img_url, price):
        auction = self.create(product_name = name, img_url= img_url, price= price )
        # do something with the book
        return auction


class Bit(models.Model):
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE)
    user  = models.ForeignKey(User, on_delete= models.CASCADE, related_name='bits')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])

    def clean(self):
        if self.price < self.auction.price:
            raise ValidationError('Bid must be greater')

    def __str__(self):
        return f"{self.user} bit {self.auction} with new price: {self.price}"


@receiver(post_save, sender= Bit)
def udate_price(sender, instance, **kwards):
        instance.auction.price = instance.price
        instance.auction.save()


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f" {self.user} about {self.auction}:{self.text[0:54]} ..."


class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchs')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='watchs')

    def __str__(self):
        return f"{self.user} watch {self.auction}"

class Category(models.Model):
    group_name = models.CharField(max_length=54)
    description = models.TextField()
