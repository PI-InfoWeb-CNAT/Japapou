from django.urls import path 
from japapou.views import *  # type: ignore
import japapou.views.delivery_man_views as views 

urlpatterns = [
    path("deliver/", delivery_man_deliver_view, name="delivery_man_deliver"),
    path("history/", delivery_man_history_view, name="delivery_man_history"),
    path("orders/", delivery_man_orders_view, name="delivery_man_orders"),
    path("profile/", delivery_man_profile_view, name="delivery_man_profile"),
    path("profile/update_user/", update_user, name="update_user"),
    path("profile/update_photo/", update_photo, name="update_photo"),
    # path("assign_delivery/<int:order_id>/", views.assign_delivery_view, name='dm_assign_delivery'),  # ERRO AQUI
    path("assign_delivery/<int:order_id>/", views.manager_assign_delivery_view, name='dm_assign_delivery'), # CORRETO
    # 1. ROTA DE SAÍDA (DISPATCH) - Nova URL para a view de Saída
    path('confirm_dispatch/<int:order_id>/', views.confirm_dispatch_view, name='dm_confirm_dispatch'), # OK
      
    # 2. ROTA DE ENTREGA (DELIVERY) - Associa a view correta de Entrega (a que criamos)
    path('confirm_delivery/<int:order_id>/', views.dm_confirm_delivery_view, name='dm_confirm_delivery'), # OK

    # mapa
    # path("mapa/", mapa_geral, name="mapa_geral"),

]