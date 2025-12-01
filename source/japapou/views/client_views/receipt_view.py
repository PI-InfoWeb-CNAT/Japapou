from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F
from japapou.models.order import Order # Assumindo a localização do seu model Order
from datetime import datetime
from django.utils import timezone

# Nota: Assumimos que a URL passa o ID do pedido. Ex: path('recibo/<int:order_id>/', views.receipt_view, name='receipt')

@login_required
def client_receipt_view(request, order_id):
    """
    Exibe o recibo de um pedido específico.
    """
    
    # 1. Obter o Pedido. Apenas o cliente que fez o pedido (ou um gerente) deve ver.
    order = get_object_or_404(
        Order.objects.select_related('usuario', 'entregador') # Otimiza o acesso a usuario e entregador
                      .prefetch_related('itens__prato'),      # Otimiza o acesso aos itens e pratos
        pk=order_id,
        usuario=request.user # Garante que apenas o próprio cliente veja o recibo
        # Se for um gerente, adicionar: | Q(usuario=request.user) | Q(usuario__tipo_usuario='MANAGER')
    )

    # 2. Detalhes Básicos
    detalhes_pedido = {
        'id': order.id,
        'nome_cliente': f"{order.usuario.first_name} {order.usuario.last_name}" if order.usuario.first_name else order.usuario.username,
        'data_criacao': order.created_at.strftime('%d/%m/%Y %H:%M'),
        'tipo_pedido': order.get_tipo_pedido_display().capitalize(), # 'Retirada' ou 'Entrega'
    }

    # 3. Detalhes dos Itens
    itens_pedido = []
    for item in order.itens.all():
        itens_pedido.append({
            'produto': item.prato.name,
            'quantidade': item.amount,
            # Use o preço_prato guardado no OrderItem
            'preco_unitario': f"{item.preco_prato:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), 
            'subtotal': f"{item.get_item_total():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        })
        
    # 4. Detalhes de Entrega/Retirada
    detalhes_entrega = {}
    
    if order.tipo_pedido == Order.TipoPedido.ENTREGA:
        detalhes_entrega['eh_entrega'] = True
        
        if order.entregador:
            # Assumindo um campo 'avaliacao_media' ou calculando uma média simples se tivéssemos um modelo de 'AvaliacaoEntregador'
            # Simulação de avaliação (você precisaria implementar a lógica real de cálculo de média):
            # Exemplo: Calculando a média de avaliações de todos os pedidos que ele entregou (LÓGICA SIMULADA)
            # avaliacao_media = order.entregador.pedidos_entregues.exclude(avaliacao__isnull=True).aggregate(Avg('avaliacao'))['avaliacao__avg']
            avaliacao_media = 4.7 # Valor Fixo para fins de demonstração

            detalhes_entrega['nome_entregador'] = f"{order.entregador.first_name} {order.entregador.last_name}" if order.entregador.first_name else order.entregador.username
            detalhes_entrega['automovel'] = order.entregador.modelo_moto or 'Não Informado'
            detalhes_entrega['cor'] = order.entregador.cor_moto or 'Não Informado'
            detalhes_entrega['placa'] = order.entregador.placa_moto or 'Não Informada'
            detalhes_entrega['avaliacao_media'] = f"{avaliacao_media:,.1f}".replace('.', ',')
        else:
            # Se o pedido ainda não foi atribuído a um entregador
            detalhes_entrega['nome_entregador'] = 'Aguardando Atribuição'
            detalhes_entrega['automovel'] = '--'
            detalhes_entrega['cor'] = '--'
            detalhes_entrega['placa'] = '--'
            detalhes_entrega['avaliacao_media'] = '--'
            
    else: # TipoPedido.RETIRADA
        detalhes_entrega['eh_entrega'] = False
        # Não precisa de detalhes de entregador/moto, mas podemos passar a info de "Pedido para:"
        detalhes_pedido['pedido_para'] = order.get_tipo_pedido_display().capitalize()
    

    # 5. Montar o Contexto
    context = {
        'order': order,
        'detalhes_pedido': detalhes_pedido,
        'itens_pedido': itens_pedido,
        'detalhes_entrega': detalhes_entrega,
        'total_final': f"{order.total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    }

    return render(request, 'client/receipt.html', context)
