from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.models import Cart, Order,OrderItem # Importar modelos necessários


@login_required
@permission_required('japapou.view_order', login_url='login')
def delivery_man_history_view(request):
    """
    View para o entregador ver seus pedidos entregues.
    """
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    # filtra os pedidos entregues do entregador logado
    # prefetch_related para otimizar a consulta dos itens e pratos relacionados
    # order_by para ordenar do mais recente para o mais antigo
    pedidos = Order.objects.filter(entregador=request.user).order_by('-created_at').prefetch_related('itens__prato')
    
    return render(request, template_name="delivery_man/history.html", context={'pedidos': pedidos}, status=200)

