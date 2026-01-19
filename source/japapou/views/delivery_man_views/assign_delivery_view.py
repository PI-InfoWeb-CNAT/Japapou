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
    '''
    Exibe os detalhes do pedido e lista de entregadores (GET); processa a escolha do entregador
    via JSON, atribui-o ao pedido e marca o status imediatamente como "ENTREGUE" (POST).
    '''

    # Busca o pedido pelo ID; retorna erro 404 se não existir.
    order = get_object_or_404(Order, id=order_id)
    
    # Busca todos os entregadores disponíveis no sistema.
    delivery_men = CustomUser.objects.filter(tipo_usuario='DELIVERY_MAN')

    # Lógica para processar a atribuição (quando o usuário clica em Salvar/Confirmar)
    if request.method == 'POST':
        try:
            # Converte os dados recebidos (JSON) para um dicionário Python.
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Dados JSON inválidos.")
            
        # Extrai o ID do entregador escolhido.
        dm_id = data.get('delivery_man_id')
        
        # Validação simples para garantir que o ID foi enviado.
        if not dm_id:
            return JsonResponse({'success': False, 'message': 'ID do entregador ausente.'}, status=400)
            
        try:
            # Verifica se o entregador existe e se é realmente do tipo 'DELIVERY_MAN'.
            dm = CustomUser.objects.get(id=dm_id, tipo_usuario='DELIVERY_MAN')
            
            # --- ATUALIZAÇÃO DO PEDIDO ---
            # 1. Vincula o entregador ao pedido.
            order.entregador = dm
            
            # 2. Define o status do pedido como ENTREGUE.
            # Nota: Isso finaliza o pedido no momento em que o entregador é escolhido.
            order.status = order.Status.ENTREGUE
            
            # Salva as alterações no banco de dados.
            order.save()
            
            return JsonResponse({'success': True})
            
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Entregador não encontrado.'}, status=404)

    # Lógica de exibição da página (GET).
    # Carrega os itens do pedido (com verificação de segurança caso 'itens' não exista).
    items = order.itens.all() if hasattr(order, 'itens') else []
    
    # Renderiza o template HTML específico, enviando os dados necessários.
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
    Processa a confirmação de entrega feita pelo entregador, atualizando o status do pedido 
    e a data de conclusão, retornando o resultado em formato JSON para o frontend.
    """
    
    try:
        # Busca o pedido no banco de dados. 
        # Usamos o try/except aqui para ter controle total sobre a mensagem de erro JSON
        # caso o pedido não exista (diferente do get_object_or_404 que retorna HTML padrão).
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Pedido não encontrado."}, status=404)
    
    # Prevenção de dupla confirmação (Idempotência).
    # Se o pedido já tiver data de entrega, não fazemos nada e apenas avisamos que já está tudo certo.
    # Isso evita erros se o entregador clicar no botão várias vezes seguidas ou se a internet falhar.
    if order.data_entrega:
        return JsonResponse({
            "status": "ok", 
            "message": "Entrega já registrada.",
            "delivery_date": order.data_entrega.isoformat() 
        }, status=200)

    # 1. Registra o momento exato da entrega usando o horário do servidor.
    order.data_entrega = timezone.now()

    # Atualiza o estado do pedido para "ENTREGUE" para que o sistema saiba que o ciclo fechou.
    order.status = order.Status.ENTREGUE
    
    # 2. Atribuição de Segurança (Fallback):
    # Se por algum motivo o pedido chegou até aqui sem um entregador vinculado no sistema,
    # assumimos que quem está a confirmar a entrega (request.user) é o responsável.
    if not order.entregador:
        order.entregador = request.user
        
    # Salva todas as alterações no banco de dados.
    order.save()

    # 3. Retorna um objeto JSON para o JavaScript do navegador.
    # O frontend vai ler "status": "ok" e poderá mostrar uma mensagem de sucesso ou 
    # mudar a cor do botão para verde, por exemplo.
    return JsonResponse({
        "status": "ok",
        "message": "Entrega registrada com sucesso.",
        "delivery_date": order.data_entrega.isoformat() 
    }, status=200)