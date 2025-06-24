from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("", home_view, name="home"),
    path("deliver", delivery_man_deliver_view, name="deliver"),
    path("history", delivery_man_history_view, name="history"),
    path("orders", delivery_man_orders_view, name="orders"),
    path("profile", delivery_man_profile_view, name="profile"),
]
