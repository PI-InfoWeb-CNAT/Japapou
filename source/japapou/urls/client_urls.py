from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("", home_view, name="home"),
    path("cart", client_cart_view, name="cart"),
    path("history", client_history_view, name="history"),
    path("menu", client_menu_view, name="menu"),
    path("order", client_order_view, name="order"),
    path("profile", client_profile_view, name="profile"),
    path("rating", client_rating_view, name="rating"),
    path("receipt", client_receipt_view, name="receipt"),
]
