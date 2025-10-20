from django.urls import path
from japapou.views import (
    manager_history_view,
    manager_menu_view,
    create_menu_view,
    manager_plates_view,
    create_plates_view,
    plate_get_json,
    plate_update_view,
    plate_delete_view,
    manager_orders_view,
    manager_profile_view,
    manager_dashboard_view,
    manager_assign_delivery_view,
)

urlpatterns = [
    path("history/", manager_history_view, name="manager_history"),
    path("menu/", manager_menu_view, name="manager_menu"),
    path("menu/create/", create_menu_view, name="create_menu"),
    path("plates/", manager_plates_view, name="manager_plates"),
    path("plates/create/", create_plates_view, name="create_plates"),
    path("plates/<int:id>/update/", plate_update_view, name="plate_update"),
    path("plates/<int:id>/delete/", plate_delete_view, name="plate_delete"),
    path("plates/json/", plate_get_json, name="plate_get_json"),
    path("orders/", manager_orders_view, name="manager_orders"),
    path("profile/", manager_profile_view, name="manager_profile"),
    path("dashboard/", manager_dashboard_view, name="manager_dashboard"),
    path("assign-delivery/", manager_assign_delivery_view, name="manager_assign_delivery"),
]
