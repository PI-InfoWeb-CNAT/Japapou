from django.urls import path  # type: ignore
from japapou.views import *  # type: ignore

urlpatterns = [
    path("history/", manager_history_view, name="manager_history"),
    path(
        "manage_delivery_man/",
        manager_manage_delivery_man_view,
        name="manage_delivery_man",
    ),
    path("menu/", manager_menu_view, name="manager_menu"),
    path("orders/", manager_orders_view, name="manager_orders"),
    path("profile/", manager_profile_view, name="manager_profile"),
    path("dashboard/", manager_dashboard_view, name="manager_dashboard"),
    path(
        "assign_delivery/", manager_assign_delivery_view, name="manager_assign_delivery"
    ),
]
