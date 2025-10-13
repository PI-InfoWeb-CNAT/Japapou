from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("cart/", client_cart_view, name="client_cart"),
    path("history/", client_history_view, name="client_history"),
    path("menu/", client_menu_view, name="client_menu"),
    path("order/", client_order_view, name="client_order"),
    path("profile/", client_profile_view, name="client_profile"),
    path("profile/update_user/", update_user, name="update_user"),
    path("profile/update_photo/", update_photo, name="update_photo"),
    path("rating/", client_rating_view, name="client_rating"),
    path("receipt/", client_receipt_view, name="client_receipt"),
]
