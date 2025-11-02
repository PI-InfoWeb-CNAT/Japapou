from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("cart/", client_cart_view, name="client_cart"),
    path("history/", client_history_view, name="client_history"),
    path("menu/", client_menu_view, name="client_menu"),
    path("order/", client_order_view, name="client_order"),
    path("profile/", client_profile_view, name="client_profile"),
    path("rating/", client_rating_view, name="client_rating"),
    path("details_plate/", details_plate_view, name="details_plate"),
    path("receipt/", client_receipt_view, name="client_receipt"),
]
