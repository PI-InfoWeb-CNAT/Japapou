# Em um arquivo de views, ex: cart_views.py

from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpRequest # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from japapou.models import Plate, Cart, CartItem # Importe os novos modelos
# (E o CustomUser, se necessário)

@login_required
def cart_view(request: HttpRequest):
    """
    Exibe o carrinho de compras do usuário logado.
    """
    # Encontra o carrinho do usuário ou cria um se não existir
    cart = Cart.objects.get_or_create(usuario=request.user)
    
    items = cart.items.all().order_by('plate__name') # Pega todos os itens do carrinho
    total = cart.get_cart_total() # Calcula o total
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    # Renderiza o template do carrinho
    return render(request, 'client/cart.html', context)


@login_required
@require_POST # Garante que esta view só aceite requisições POST
def add_to_cart_view(request: HttpRequest):
    """
    Adiciona um prato ao carrinho.
    Espera um 'plate_id' e 'quantity' no POST.
    """
    plate_id = request.POST.get('plate_id') # tenta pegar o id do prato passado no post
    
    quantity = int(request.POST.get('quantity', 1)) # Pega a quantidade do formulário, com padrão 1
    
    if not plate_id:
        # Lógica de erro caso o prato não exista
        return redirect('alguma_pagina_de_erro_ou_anterior')

    plate = get_object_or_404(Plate, id=plate_id) # pega o objeto pelo id ou exibe um erro 404
    cart, cart_created = Cart.objects.get_or_create(usuario=request.user)
    
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