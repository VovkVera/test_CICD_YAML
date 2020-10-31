from django.contrib import admin

from .models import Auction, Bit, Comment, Watch

admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bit)
admin.site.register(Watch)


