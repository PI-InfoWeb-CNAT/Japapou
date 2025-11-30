from django.urls import path  # type: ignore
from japapou.views.client_views import *  # type: ignore
from japapou.views.client_views.cart_view import add_to_cart_view, remove_from_cart_view, update_cart_item_view  # type: ignore

urlpatterns = [
    path("menu/", client_menu_view, name="client_menu"),
    path("order/", client_order_view, name="client_order"),
    path("profile/", client_profile_view, name="client_profile"),
    path("profile/update_user/", update_user, name="update_user"),
    path("profile/update_photo/", update_photo, name="update_photo"),
    path("rating/", client_rating_view, name="client_rating"),
    path("details_plate/<int:plate_id>/", details_plate_view, name="details_plate"),
    path("details_plate/<int:plate_id>/review/", rating_view, name="rating"),
    path("receipt/", client_receipt_view, name="client_receipt"),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/', add_to_cart_view, name='add_to_cart'),
    path('cart/remove/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/', update_cart_item_view, name='update_cart_item'),
    #path('order/create/', order_view.create_order_view, name='create_order'),
    path('orders/', order_view.client_order_view, name='client_history'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/adicionar-endereco/', add_endereco_view, name='add_endereco'),
    path('order/sucesso/<int:order_id>/', order_success_view, name='order_success'),

]
