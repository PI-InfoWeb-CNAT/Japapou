from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from japapou.models.order_item import OrderItem
from japapou.models.order import Order_Pickup
from django.utils import timezone
import json

@login_required
@permission_required('view_order', login_url='home')
@csrf_exempt
def manager_assign_pickup_view(request, order_id):
    order = get_object_or_404(Order_Pickup, id=order_id)

    if request.method == 'POST':
        # Marca a retirada
        order.pickup_date = timezone.now()
        order.save()
        return JsonResponse({
            "status": "ok",
            "pickup_date": order.pickup_date.strftime("%d/%m/%Y %H:%M")
        })

    items = order.items.all() if hasattr(order, 'items') else []

    return render(request, 'manager/assign_pickup.html', {
        'order': order,
        'items': items,
        'user': getattr(order, 'user', None)
    })

@login_required
@permission_required('change_order', raise_exception=True)
@require_POST
def confirm_pickup_view(request, order_id):
    from japapou.models.order import Order_Pickup

    try:
        order = Order_Pickup.objects.get(id=order_id)
    except Order_Pickup.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Pedido não encontrado"}, status=404)

    order.pickup_date = timezone.now()
    order.save()

    return JsonResponse({
        "status": "ok",
        "pickup_date": order.pickup_date.strftime("%d/%m/%Y %H:%M")
    })
