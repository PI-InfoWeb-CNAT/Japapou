from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpRequest # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from japapou.models import Plate, Cart, CartItem, Order # Importe os novos modelos
from decimal import Decimal
import json
from django.db import transaction # Importar transaction

# (E o CustomUser, se necessário)

TAXA_ENTREGA = 5.0

@login_required
def cart_view(request: HttpRequest):
    """
    Exibe o carrinho de compras do usuário logado.
    """
    # Encontra o carrinho do usuário ou cria um se não existir
    cart, created = Cart.objects.get_or_create(usuario=request.user)
    
    items = cart.items.all().order_by('plate__name') # Pega todos os itens do carrinho
    total = cart.get_cart_total() # Calcula o total

    dados_js = {
        "taxa_entrega": TAXA_ENTREGA
    }
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
        'taxa': TAXA_ENTREGA,
        'dados_js': json.dumps(dados_js)
    }
    # Renderiza o template do carrinho
    return render(request, 'client/cart.html', context)


@login_required
@require_POST # Garante que esta view só aceite requisições POST
@transaction.atomic # Garante que todas as operações sejam atômicas
def add_to_cart_view(request: HttpRequest):
    """
    Adiciona um prato ou um pedido inteiro ao carrinho.
    Espera um 'plate_id' e 'quantity' (para item único) OU 'order_id' (para re-pedido).
    """
    cart, _ = Cart.objects.get_or_create(usuario=request.user)
    
    order_id = request.POST.get('order_id')
    
    if order_id:
        # Lógica para adicionar um PEDIDO INTEIRO (Re-pedido)
        try:
            # Garante que o pedido existe e pertence ao usuário
            order_to_copy = get_object_or_404(Order, id=order_id, usuario=request.user)
            order_items = order_to_copy.itens.all()

            for order_item in order_items:
                # Tenta encontrar o item no carrinho
                cart_item, item_created = CartItem.objects.get_or_create(
                    cart=cart,
                    plate=order_item.prato, # Usa o prato do OrderItem
                    defaults={'quantity': order_item.amount} # Usa a quantidade do OrderItem se for novo
                )
                
                if not item_created:
                    # Se o item já existe, soma a quantidade do pedido antigo
                    cart_item.quantity += order_item.amount 
                    cart_item.save()
            
            # Redireciona para o carrinho após adicionar o pedido completo
            return redirect('cart_view')

        except Order.DoesNotExist:
            # Caso o order_id seja inválido ou não pertença ao usuário
            # Retorna para a página de histórico (ou uma página de erro)
            return redirect('client_history')


    # Lógica para adicionar um ITEM ÚNICO (Original)
    plate_id = request.POST.get('plate_id') 
    quantity = int(request.POST.get('quantity', 1))
    
    if not plate_id:
        # Se nem plate_id nem order_id foram fornecidos
        return redirect('client_menu') # Redireciona para o menu ou página inicial

    plate = get_object_or_404(Plate, id=plate_id)
    
    # Tenta encontrar o item no carrinho
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        plate=plate,
        # 'defaults' só é usado se o item está sendo criado
        defaults={'quantity': quantity}
    )
    
    if not item_created: #
        # Se o item já existia, apenas atualiza a quantidade
        cart_item.quantity += quantity 
        cart_item.save()
        
    
    return redirect('cart_view')


@login_required
@require_POST
def remove_from_cart_view(request: HttpRequest):
    """
    Remove um item completamente do carrinho.
    Espera um 'item_id' (ID do CartItem) no POST.
    """
    item_id = request.POST.get('item_id')
    
    # Busca o item, garantindo que ele pertence ao carrinho do usuário logado
    cart_item = get_object_or_404(
        CartItem, 
        id=item_id, 
        cart__usuario=request.user
    )
    
    cart_item.delete()
    
    return redirect('cart_view')


@login_required
@require_POST
def update_cart_item_view(request: HttpRequest):
    """
    Atualiza a quantidade de um item no carrinho.
    Espera 'item_id' e 'quantity' no POST.
    """
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1)) # Pega a nova quantidade total
    
    cart_item = get_object_or_404(
        CartItem, 
        id=item_id, 
        cart__usuario=request.user
    )
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        # Se a quantidade for 0 ou menos, remove o item
        cart_item.delete()
        
    return redirect('cart_view')