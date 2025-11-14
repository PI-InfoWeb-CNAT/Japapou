from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.views.decorators.http import require_POST
#from django.views.decorators.csrf import csrf_exempt
from japapou.models.order import Order
from datetime import datetime
import pytz

@login_required
@permission_required('view_order', login_url='home')
def manager_assign_pickup_view(request, order_id):
    '''View para carregar a pagina de pedidos para o gerente'''

    timezone = pytz.timezone('America/Sao_Paulo')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Marca a retirada
        order.data_retirada = datetime.now(timezone)
        order.save()
        return JsonResponse({
            "status": "ok",
            "pickup_date": order.data_retirada.strftime("%d/%m/%Y %H:%M")
        })

    items = order.itens.all() if hasattr(order, 'itens') else []

    return render(request, 'manager/assign_pickup.html', {
        'order': order,
        'items': items,
        'user': getattr(order, 'user', None)
    })

@login_required
@permission_required('change_order', raise_exception=True)
@require_POST
def confirm_pickup_view(request, order_id):
    '''View para o gerente confirmar a retirada de um pedido'''
    timezone = pytz.timezone('America/Sao_Paulo')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Pedido não encontrado"}, status=404)

    order.data_retirada = datetime.now(timezone)
    order.save()

    return JsonResponse({
        "status": "ok",
        "pickup_date": order.data_retirada.strftime("%d/%m/%Y %H:%M")
    })