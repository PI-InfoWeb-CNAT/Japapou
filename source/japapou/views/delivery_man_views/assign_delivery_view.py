from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from japapou.models.order_item import OrderItem
from japapou.models.order import Order_Delivery
from django.utils import timezone
import json

@login_required
@permission_required('view_order', login_url='home')
@csrf_exempt
def delivery_man_confirm_delivery_view(request, order_id):
    """
    View para exibir o pedido e registrar a entrega (delivery_date).
    """
    order = get_object_or_404(Order_Delivery, id=order_id)
    items = order.items.all() if hasattr(order, 'items') else []

    if request.method == 'POST':
        # Marca como entregue
        order.delivery_date = timezone.now()
        order.save()
        return JsonResponse({
            "status": "ok",
            "delivery_date": order.delivery_date.strftime("%d/%m/%Y %H:%M")
        })

    return render(request, 'delivery_man/assign_delivery.html', {
        'order': order,
        'items': items,
        'user': getattr(order, 'user', None)
    })
