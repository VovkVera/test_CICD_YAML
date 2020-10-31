from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("add", views.add, name="add"),
    path("add_wach", views.add_to_watchlist, name="add_to_watchlist"),
    path("del_wach", views.del_from_watchlist, name="del_from_watch"),
    path("bid", views.bid, name="bid"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:auction_id>", views.auction_page, name="auction"),
    path("auctions/<str:category>", views.category_page, name="category"),
    path("auctions/<str:auction_id>/leave_comment", views.leave_comment, name="leave_comment"),
]
