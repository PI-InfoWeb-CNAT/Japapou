from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("deliver/", delivery_man_deliver_view, name="delivery_man_deliver"),
    path("history/", delivery_man_history_view, name="delivery_man_history"),
    path("orders/", delivery_man_orders_view, name="delivery_man_orders"),
    path("profile/", delivery_man_profile_view, name="delivery_man_profile"),
]
