# order_view.py

from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required, permission_required # type: ignore
from django.db import transaction # Importar transaction
from django.utils import timezone # Importar timezone
from japapou.models import Cart, Order,OrderItem # Importar modelos necessários


@login_required
@permission_required('japapou.view_order', login_url='login')
def client_order_view(request):
    """
    View para o cliente ver seus próprios pedidos.
    """
    
    if request.user.tipo_usuario != "CLIENT":
        return render(request, "403.html", status=403)

    # Lógica para buscar os pedidos do cliente
    pedidos = Order.objects.filter(usuario=request.user).order_by('-created_at')

    return render(request, template_name="client/history.html", context={'pedidos': pedidos}, status=200)



@login_required
@transaction.atomic 
def create_order_view(request):
    """
    Processa o checkout 
    """
    
    if request.method != "POST":
        return redirect('cart_view') 

    
    try:
        cart = request.user.cart 
        cart_items = cart.items.all() 
    except Cart.DoesNotExist:
        
        return redirect('home_page') 

    
    if not cart_items.exists():
        # Adicione uma mensagem de erro aqui se quiser
        return redirect('cart_view')

    
    try:
        
        total = cart.get_cart_total()

        
        new_order = Order.objects.create(
            usuario=request.user,
            total=total,
            estimate=total 
            
        )

        
        items_para_criar = []
        for item in cart_items:
            items_para_criar.append(
                OrderItem(
                    order=new_order,
                    prato=item.plate,
                    amount=item.quantity,
                    comment="" # Adicione lógica se permitir comentários no carrinho
                )
            )
        
        
        OrderItem.objects.bulk_create(items_para_criar)

        
        cart_items.delete()

        
        return redirect('client_order_view')

    except Exception as e:
        # Se qualquer passo falhar, a transação é revertida
        return redirect('cart_view')