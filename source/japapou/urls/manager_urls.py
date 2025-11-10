from django.urls import path
# Importa o pacote de views do Manager (assumindo que ele está corretamente mapeado)
import japapou.views.manager_views as views 
# Note: Isso pressupõe que suas views de fato estão dentro de japapou/views/manager_views.py ou __init__.py

urlpatterns = [

    # DELIVERY MAN (Motoboys/Entregadores)
    path("delivery-man/", views.manage_delivery_man_view, name="manager_delivery_man"),
    path("delivery-man/create/", views.manager_delivery_man_create_view, name="manager_delivery_man_create"),
    path("delivery-man/<int:id>/", views.manager_delivery_man_detail_view, name="manager_delivery_man_detail"),
    path("delivery-man/<int:id>/edit/", views.manager_delivery_man_update_view, name="manager_delivery_man_update"),
    path("delivery-man/<int:id>/delete/", views.manager_delivery_man_delete_view, name="manager_delivery_man_delete"),

    # MENUS
    path("menu/", views.manager_menu_view, name="manager_menu"),
    path("menu/create/", views.create_menu_view, name="create_menu"),

    # PLATES (Pratos)
    path("plates/", views.manager_plates_view, name="manager_plates"),
    path("plates/create/", views.create_plates_view, name="create_plates"),
    path("plates/<int:id>/update/", views.plate_update_view, name="plate_update"),
    path("plates/<int:id>/json", views.plate_get_json, name="plate_json"),
    path("plates/<int:id>/delete/", views.plate_delete_view, name="plate_delete"),
    path("plates/json/", views.plate_get_json, name="plate_get_json"), # JSON API

    # GERAIS
    path("history/", views.manager_history_view, name="manager_history"),
    path("orders/", views.manager_orders_view, name="manager_orders"),
    path("profile/", views.manager_profile_view, name="manager_profile"),
    path("dashboard/", views.manager_dashboard_view, name="manager_dashboard"),
    path("assign-delivery/", views.manager_assign_delivery_view, name="manager_assign_delivery"),
]
