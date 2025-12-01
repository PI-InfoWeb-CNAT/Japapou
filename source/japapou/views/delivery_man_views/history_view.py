from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.models import Cart, Order,OrderItem # Importar modelos necessários

@login_required
@permission_required('japapou.view_order', login_url='login')
def delivery_man_history_view(request):
    """
    View para o cliente ver seus próprios pedidos feitos.
    """
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    pedidos = Order.objects.filter(entregador=request.user).order_by('-created_at').prefetch_related('itens__prato')
    
    return render(request, template_name="delivery_man/history.html", context={'pedidos': pedidos}, status=200)

