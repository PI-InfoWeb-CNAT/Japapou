from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# from japapou.models.order_item import OrderItem # Não está sendo usado diretamente aqui
from japapou.models.order import Order # <-- MODELO CORRIGIDO (Order em vez de Order_Delivery)
from japapou.models import CustomUser
from django.utils import timezone 
import json

@login_required
# @permission_required('view_order', login_url='home')
@csrf_exempt
def manager_assign_delivery_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    delivery_men = CustomUser.objects.filter(tipo_usuario='DELIVERY_MAN')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Dados JSON inválidos.")
            
        dm_id = data.get('delivery_man_id')
        
        if not dm_id:
            return JsonResponse({'success': False, 'message': 'ID do entregador ausente.'}, status=400)
            
        try:
            dm = CustomUser.objects.get(id=dm_id, tipo_usuario='DELIVERY_MAN')
            
            order.entregador = dm
            order.status = order.Status.ENTREGUE
            order.save()
            return JsonResponse({'success': True})
            
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Entregador não encontrado.'}, status=404)

    items = order.itens.all() if hasattr(order, 'itens') else []
    
    return render(request, 'delivery_man/assign_delivery.html', {
        'order': order,
        'items': items,
        'delivery_men': delivery_men,
        'entregador_atribuido': order.entregador, 
        'usuario': order.usuario 
    })

@login_required(login_url='/login/')
# @permission_required(['japapou.change_order'], raise_exception=True) 
@require_POST
def confirm_dispatch_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest("Pedido não encontrado.")
    
    order.data_saida = timezone.now()
    order.save()

    return JsonResponse({
        "status": "ok",
        "dispatch_date": order.data_saida.strftime("%d/%m/%Y %H:%M")
    })

@login_required(login_url='/login/')
# @permission_required(['japapou.change_order'], raise_exception=True)
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

    order.status = order.Status.ENTREGUE
    
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