from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.models import Order # Importar modelos necessários
import json


@login_required
@permission_required('japapou.view_order', login_url='login')
def delivery_man_orders_view(request):
    """
    View para o Entregador ver os pedidos pendentes.
    """
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    pedidos = Order.objects.filter(entregador_id=request.user.id).order_by('-created_at').prefetch_related('itens__prato')

    # print(pedidos)
    
    return render(request, template_name="delivery_man/orders.html", context={'pedidos': pedidos}, status=200)

def mapa_geral(request):
    pedidos = Order.objects.filter(entregador_id=request.user.id).order_by('-created_at').prefetch_related('itens__prato')

    lista_pedidos = []

    for p in pedidos:
        lista_pedidos.append({
            'cliente': p.cliente,
            'lat': p.lat_destino,
            'lon': p.lon_destino,
            'id': p.id
        })
    
    pedidos_json = json.dumps(lista_pedidos)

    render(request, "map.html", context={"pedidos_json": pedidos_json})

