from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Avg, F
from django.http import JsonResponse
# Importa o modelo Order. Substitua 'japapou.models.order' pelo caminho correto se for diferente.
from japapou.models.order import Order 
# NOVO: Importa PlateReview do módulo de reviews
from japapou.models.review import CourierReview, PlateReview 
from japapou.models.user import CustomUser 
import json
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# A função round() é embutida no Python e não precisa de importação de 'math'.
# A função floor() não está sendo utilizada, portanto, o import foi removido.


# ------------------------------------------------
# 1. VIEW DE SUBMISSÃO DA AVALIAÇÃO (API/AJAX)
# ------------------------------------------------

@login_required
@require_POST
def submit_courier_review(request):
  """
  Recebe a avaliação do entregador via AJAX (Fetch) e salva no banco de dados.
  Esta função também recalcula a média e a retorna.
  """
  try:
    # Tenta carregar o JSON do corpo da requisição
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'message': 'Erro no formato JSON da requisição.'}, status=400)

  # 1. Extração e Validação dos Dados
  rating_value = data.get('rating')
  comment = data.get('comment', '').strip()
  entregador_id = data.get('entregador_id')

  if not rating_value or not entregador_id:
    return JsonResponse({'message': 'Nota (rating) ou ID do entregador não fornecidos.'}, status=400)
  
  try:
    rating_value = int(rating_value)
    entregador_id = int(entregador_id)
    if not 1 <= rating_value <= 5:
      return JsonResponse({'message': 'A nota deve ser entre 1 e 5.'}, status=400)
  except ValueError:
    return JsonResponse({'message': 'Nota ou ID do entregador inválidos.'}, status=400)

  # 2. Busca do Entregador
  try:
    entregador = CustomUser.objects.get(pk=entregador_id) 
  except ObjectDoesNotExist:
    return JsonResponse({'message': 'Entregador não encontrado.'}, status=404)

  # 3. Verifica se o usuário já avaliou este entregador
  if CourierReview.objects.filter(usuario=request.user, entregador=entregador).exists():
    # Retorna 409 Conflito para indicar que a avaliação já existe e não foi salva.
    return JsonResponse({'message': 'Você já avaliou este entregador anteriormente.'}, status=409)

  # 4. Criação da Avaliação
  try:
    CourierReview.objects.create(
      usuario=request.user,
      entregador=entregador,
      value=rating_value,
      comment=comment
    )
    # Opcional: Recalcula a média e retorna
    media_query = CourierReview.objects.filter(entregador=entregador).aggregate(Avg('value'))
    # A nova média é calculada e retornada
    nova_media_str = f"{media_query.get('value__avg'):.1f}".replace('.', ',') if media_query.get('value__avg') else '--'
    
    return JsonResponse({
      'message': 'Avaliação enviada com sucesso!', 
      'new_average': nova_media_str
    }, status=201)
  
  except Exception as e:
    print(f"Erro ao salvar avaliação: {e}")
    return JsonResponse({'message': 'Erro interno ao processar a avaliação.'}, status=500)


# ------------------------------------------------
# 2. VIEW DO RECIBO (MODIFICADA)
# ------------------------------------------------

@login_required
def client_receipt_view(request, order_id):
  """
  Exibe o recibo de um pedido específico.
  Inclui lógica para filtrar pratos já avaliados.
  """
  
  order = get_object_or_404(
    Order.objects.select_related('usuario', 'entregador')
          .prefetch_related('itens__prato'),
    pk=order_id,
    usuario=request.user
  )

  detalhes_pedido = {
    'id': order.id,
    'nome_cliente': f"{order.usuario.first_name} {order.usuario.last_name}" if order.usuario.first_name else order.usuario.username,
    'data_criacao': order.created_at.strftime('%d/%m/%Y %H:%M'),
    'tipo_pedido': order.get_tipo_pedido_display().capitalize(),
  }

  # --- Lógica de Filtragem de Pratos Já Avaliados (NOVO) ---
  # Pega os IDs de todos os pratos (plates) que o usuário JÁ avaliou.
  pratos_ja_avaliados_ids = PlateReview.objects.filter(
    usuario=request.user
  ).values_list('plate__pk', flat=True)
  
  itens_pedido = []
  # Lista que será passada para o modal, contendo apenas itens AINDA NÃO AVALIADOS
  itens_para_avaliar = [] 
  
  # Assumindo que o related_name de OrderItem para Order é 'itens'
  for item in order.itens.all():
    # Lógica para formatação de moeda em português (ex: 1.234,56)
    preco_unitario_formatado = f"{item.preco_prato:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    subtotal_formatado = f"{item.get_item_total():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    item_data = {
      'produto': item.prato.name,
      'quantidade': item.amount,
      'preco_unitario': preco_unitario_formatado,
      'subtotal': subtotal_formatado,
      'prato_id': item.prato.pk,
    }
    
    itens_pedido.append(item_data)
    
    # Adiciona o item na lista de 'itens_para_avaliar' SE ele tiver um prato_id 
    # e SE o ID do prato AINDA NÃO estiver na lista de pratos já avaliados.
    if item.prato and item.prato.pk not in pratos_ja_avaliados_ids:
      itens_para_avaliar.append(item_data)


  # --- Lógica de Detalhes da Entrega (Mantida) ---
  detalhes_entrega = {
    'eh_entrega': order.tipo_pedido == Order.TipoPedido.ENTREGA,
    'mostrar_modal_avaliacao': False 
  }
  
  if detalhes_entrega['eh_entrega']:
    if order.entregador:
      entregador = order.entregador
      
      # 1. Calcula a Média REAL e Arredonda
      media_query = CourierReview.objects.filter(entregador=entregador).aggregate(Avg('value'))
      avaliacao_media = media_query.get('value__avg')
      
      if avaliacao_media is None:
        avaliacao_media_formatada = '--'
        avaliacao_media_arredondada = 0 # 0 estrelas para renderização
      else:
        avaliacao_media_formatada = f"{avaliacao_media:,.1f}".replace('.', ',')
        # Arredonda a média para o número inteiro mais próximo (ex: 4.3 -> 4, 4.6 -> 5)
        avaliacao_media_arredondada = int(round(avaliacao_media)) 

      # Verifica se o cliente JÁ AVALIOU este entregador
      avaliacao_existente = CourierReview.objects.filter(
        usuario=request.user, 
        entregador=entregador
      ).exists()
      
      # === CORREÇÃO DO ERRO 'order_set' ===
      num_entregas_simulado = Order.objects.filter(
        entregador=entregador,
        tipo_pedido=Order.TipoPedido.ENTREGA # Contamos apenas entregas
      ).count()

      # === DADOS DO ENTREGADOR ===
      detalhes_entrega['entregador_id'] = entregador.pk
      detalhes_entrega['nome_entregador'] = f"{entregador.first_name} {entregador.last_name}" if entregador.first_name else entregador.username
      detalhes_entrega['automovel'] = entregador.modelo_moto or 'Não Informado'
      detalhes_entrega['cor'] = entregador.cor_moto or 'Não Informada'
      detalhes_entrega['placa'] = entregador.placa_moto or 'Não Informada'
      detalhes_entrega['avaliacao_media'] = avaliacao_media_formatada    # Exibe '4,3'
      detalhes_entrega['avaliacao_media_arredondada'] = avaliacao_media_arredondada # Exibe '4' (para lógica de estrelas)
      
      detalhes_entrega['data_ingresso'] = entregador.date_joined.strftime('%d/%m/%Y') if entregador.date_joined else 'N/A'
      detalhes_entrega['num_entregas'] = num_entregas_simulado 
      
      detalhes_entrega['mostrar_modal_avaliacao'] = not avaliacao_existente
      
    else:
      # Caso não haja entregador
      detalhes_entrega.update({
        'nome_entregador': 'Aguardando Atribuição',
        'automovel': '--', 'cor': '--', 'placa': '--',
        'avaliacao_media': '--',
        'avaliacao_media_arredondada': 0, 
        'data_ingresso': '--',
        'num_entregas': '--',
        'entregador_id': None,
        'mostrar_modal_avaliacao': False
      })
      
  else: # TipoPedido.RETIRADA
    detalhes_pedido['pedido_para'] = order.get_tipo_pedido_display().capitalize()
  

  # --- Controle do Modal de Pratos (NOVO) ---
  # O modal de pratos só deve ser exibido se houver itens para avaliar.
  mostrar_modal_pratos = bool(itens_para_avaliar)

  context = {
    'order': order,
    'detalhes_pedido': detalhes_pedido,
    'itens_pedido': itens_pedido, # Lista completa para o recibo principal
    'itens_para_avaliar': itens_para_avaliar, # Lista filtrada para o modal de pratos
    'mostrar_modal_pratos': mostrar_modal_pratos, # Flag para renderizar e abrir o modal
    'detalhes_entrega': detalhes_entrega,
    'total_final': f"{order.total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
  }

  return render(request, 'client/receipt.html', context)

