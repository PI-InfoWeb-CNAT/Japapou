from django.shortcuts import render, get_object_or_404  # type: ignore
from django.contrib.auth.decorators import permission_required, login_required
from japapou.models.order import Order_Delivery
from japapou.models.order_item import OrderItem



@login_required
@permission_required('view_order', login_url='home')
def manager_assign_delivery_view(request, order_id):
    order = get_object_or_404(Order_Delivery, id=order_id)
    items = OrderItem.objects.filter(order=order)  # precisa ter FK order no modelo!

    context = {
        'order': order,
        'items': items,
        'delivery_man': order.delivery_man,
    }
    return render(request, 'manager/assign_delivery.html', context)
