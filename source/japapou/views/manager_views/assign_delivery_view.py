from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from japapou.models.order_item import OrderItem
from japapou.models.order import Order_Delivery
from japapou.models import CustomUser
from django.utils import timezone 
import json

@login_required
@permission_required('view_order', login_url='home')
@csrf_exempt
def manager_assign_delivery_view(request, order_id):
    order = Order_Delivery.objects.get(id=order_id)
    delivery_men = CustomUser.objects.filter(tipo_usuario='DELIVERY_MAN')

    if request.method == 'POST':
        data = json.loads(request.body)
        dm_id = data.get('delivery_man_id')
        try:
            dm = CustomUser.objects.get(id=dm_id, tipo_usuario='DELIVERY_MAN')
            order.delivery_man = dm
            order.save()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False})

    items = order.items.all()
    return render(request, 'manager/assign_delivery.html', {
        'order': order,
        'items': items,
        'delivery_men': delivery_men,
        'delivery_man': order.delivery_man,
        'user': order.user if hasattr(order, 'user') else None
    })


@login_required(login_url='/login/')
@permission_required(['japapou.change_order_delivery'], raise_exception=True)
@require_POST
def confirm_dispatch_view(request, order_id):
    try:
        order = Order_Delivery.objects.get(id=order_id)
    except Order_Delivery.DoesNotExist:
        return HttpResponseBadRequest("Pedido não encontrado.")

    # Atualiza a data/hora de saída
    order.dispatch_date = timezone.now()
    order.save()

    return JsonResponse({
        "status": "ok",
        "dispatch_date": order.dispatch_date.strftime("%d/%m/%Y %H:%M")
    })

