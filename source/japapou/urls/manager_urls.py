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
    path("menu/create/", create_menu_view, name="create_menu"),
    path("plates/", manager_plates_view, name="manager_plates"),
    path("plates/create", create_plates_view, name="create_plates_view"),
    path("plates/<int:id>/edit/", plate_get_json, name="manager_plates_edit"),
    path("plates/<int:id>/update/", plate_update_view, name="manager_plates_update"),
    path("plates/<int:id>/delete/", plate_delete_view, name="manager_plate_delete"),
    path("orders/", manager_orders_view, name="manager_orders"),
    path("profile/", manager_profile_view, name="manager_profile"),
    path("profile/update_user/", update_user, name="update_user"),
    path("profile/update_photo/", update_photo, name="update_photo"),
    path("dashboard/", manager_dashboard_view, name="manager_dashboard"),
    path("assign_delivery/", manager_assign_delivery_view, name="manager_assign_delivery"),
    path("register_delivery_man/", delivery_man_register_view, name="register_delivery_man"),
]
