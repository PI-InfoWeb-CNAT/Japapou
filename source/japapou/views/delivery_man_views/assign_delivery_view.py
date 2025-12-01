from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone 
from japapou.models.order import Order # Certifique-se de que o modelo Order está importado

# ... outras views ...

@login_required(login_url='/login/')
@permission_required(['japapou.change_order'], raise_exception=True) 
@require_POST
def dm_confirm_delivery_view(request, order_id):
    """
    Registra a data de entrega (data_entrega) do pedido.
    Esta é a view que o JavaScript está chamando via POST.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Pedido não encontrado."}, status=404)
    
    # Prevenção de dupla confirmação
    if order.data_entrega:
        return JsonResponse({
            "status": "ok", 
            "message": "Entrega já registrada.",
            "delivery_date": order.data_entrega.isoformat() 
        }, status=200)

    # 1. Registra a entrega
    order.data_entrega = timezone.now()
    
    # 2. Opcional: Atribui o entregador se não estiver definido
    if not order.entregador:
        order.entregador = request.user
        
    order.save()

    # 3. Retorna sucesso para o JavaScript
    return JsonResponse({
        "status": "ok",
        "message": "Entrega registrada com sucesso.",
        "delivery_date": order.data_entrega.isoformat() 
    }, status=200)