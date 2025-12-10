from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.models import Order # Importar modelos necessários
from django.conf import settings
import json

@login_required
@permission_required('japapou.view_order', login_url='login')
def delivery_man_orders_view(request):
    """
    View para o Entregador ver os pedidos pendentes.
    """
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    pedidos_pendentes = Order.objects.filter(entregador_id=request.user.id).order_by('-created_at').prefetch_related('itens__prato')


    lista_para_mapa = []

    for pedido in pedidos_pendentes:
        # Verifica se o pedido é de ENTREGA e se tem endereço com coordenadas
        if (pedido.tipo_pedido == 'ENTREGA' and 
            pedido.endereco_entrega and 
            pedido.endereco_entrega.lat_destino):
            
            endereco = pedido.endereco_entrega
            
            lista_para_mapa.append({
                'id': pedido.id,
                'cliente': pedido.usuario.username,
                'lat': endereco.lat_destino,
                'lon': endereco.lon_destino,
                'endereco': f"{endereco.logradouro}, {endereco.numero}, {endereco.bairro}",
            })

    mapa_json = json.dumps(lista_para_mapa)

    
    
    return render(request, template_name="delivery_man/orders.html", context={'pedidos': pedidos_pendentes, 'mapa_json': mapa_json, 'TOMTOM_KEY':settings.TOMTOM_KEY}, status=200)



