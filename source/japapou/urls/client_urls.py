from django.urls import path 
from japapou.views.client_views import *  
from japapou.views.client_views.cart_view import add_to_cart_view, remove_from_cart_view, update_cart_item_view  # type: ignore
from japapou.views.client_views.receipt_view import submit_courier_review

urlpatterns = [
    path("menu/", client_menu_view, name="client_menu"),
    path("order/", client_order_view, name="client_order"),
    path("profile/", client_profile_view, name="client_profile"),
    path("profile/update_user/", update_user, name="update_user"),
    path("rating/", client_rating_view, name="client_rating"),
    path("details_plate/<int:plate_id>/", details_plate_view, name="details_plate"),
    path("details_plate/review/<int:plate_id>/", rating_view, name="rating"),
    path('review/edit/<int:review_id>/', edit_review_view, name='edit_review'),
    path('review/delete/<int:review_id>/', delete_review_view, name='delete_review'),
    path("receipt/<int:order_id>", client_receipt_view, name="client_receipt"),
    
    # Rota API/AJAX para submeter a avaliação do entregador (CourierReview)
    # Deve ser o mesmo URL usado na função fetch do JavaScript: '/api/review/courier/'
    path('api/review/courier/', submit_courier_review, name='submit_courier_review'), # <--- NOVO
    
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