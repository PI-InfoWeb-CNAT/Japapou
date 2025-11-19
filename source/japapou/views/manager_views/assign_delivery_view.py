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
@permission_required('view_order', login_url='home')
@csrf_exempt
def manager_assign_delivery_view(request, order_id):
    # 1. Usar Order no lugar de Order_Delivery
    order = get_object_or_404(Order, id=order_id)
    
    # Busca entregadores
    delivery_men = CustomUser.objects.filter(tipo_usuario='DELIVERY_MAN')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Dados JSON inválidos.")
            
        dm_id = data.get('delivery_man_id')
        
        # Validação de ID
        if not dm_id:
            return JsonResponse({'success': False, 'message': 'ID do entregador ausente.'}, status=400)
            
        try:
            dm = CustomUser.objects.get(id=dm_id, tipo_usuario='DELIVERY_MAN')
            
            # 2. Corrigido: usando o campo 'entregador'
            order.entregador = dm
            order.save()
            return JsonResponse({'success': True})
            
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Entregador não encontrado.'}, status=404)

    # 3. Tentativa: usando 'itens' como related_name para OrderItem
    # Se 'itens' não funcionar, verifique o related_name no seu modelo OrderItem
    items = order.itens.all() if hasattr(order, 'itens') else []
    
    return render(request, 'manager/assign_delivery.html', {
        'order': order,
        'items': items,
        'delivery_men': delivery_men,
        # 4. Corrigido: usando o campo 'entregador'
        'entregador_atribuido': order.entregador, 
        # 5. Corrigido: usando o campo 'usuario'
        'usuario': order.usuario 
    })


# ---------------------------------------------------------------------------------------------------

@login_required(login_url='/login/')
@permission_required(['japapou.change_order'], raise_exception=True) # <-- Permissão ajustada para Order
@require_POST
def confirm_dispatch_view(request, order_id):
    try:
        # 1. Usar Order no lugar de Order_Delivery
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest("Pedido não encontrado.")
    
    # 2. Corrigido: usando o campo 'data_saida'
    # Atualiza a data/hora de saída
    order.data_saida = timezone.now()
    order.save()

    return JsonResponse({
        "status": "ok",
        # 3. Corrigido: usando o campo 'data_saida' para formatar
        "dispatch_date": order.data_saida.strftime("%d/%m/%Y %H:%M")
    })