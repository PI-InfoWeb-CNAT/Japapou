from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("", home_view, name="home"),
    path("history", manager_history_view, name="history"),
    path(
        "manage_delivery_man",
        manager_manage_delivery_man_view,
        name="manage_delivery_man",
    ),
    path("manage_menu", manager_manage_menu_view, name="manage_menu"),
    path("manage_orders", manager_orders_view, name="manage_orders"),
    path("profile", manager_profile_view, name="profile"),
    path("reports", manager_reports_view, name="reports"),
]
