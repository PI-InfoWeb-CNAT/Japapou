from django.shortcuts import render # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from japapou.models import Order # Importamos o modelo Order
# (Assumindo que OrderItem e Plate serão acessados via 'related_name')

@login_required # Garante que apenas usuários logados possam ver esta página
def client_history_view(request):
    """
    Exibe o histórico de pedidos finalizados do cliente logado.
    """
    
    if request.user.tipo_usuario != 'CLIENT':
        return render(request, "403.html", status=403)

   
    
    pedidos_do_cliente = OrderPickup.objects.filter(
        usuario=request.user
    ).prefetch_related(
        'items', 'items__prato' 
    ).order_by('-created_at') 

    
    context = {
        'pedidos': pedidos_do_cliente
    }
    
    
    return render(request, template_name="client/history.html", context=context, status=200)