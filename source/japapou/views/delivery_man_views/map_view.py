from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from japapou.models import Order # Importar modelos necessários
from django.conf import settings
import json


@login_required
def mapa_geral(request):
    pedidos_pendentes = Order.objects.filter(
        status='PROCESSANDO',
        endereco_entrega__lat_destino__isnull=False
    ).select_related('endereco_entrega') # pedidos pendentes com um endereço de entrega

    lista_para_mapa = []

    for pedido in pedidos_pendentes:

        endereco = pedido.endereco_entrega

        lista_para_mapa.append({
            'id_pedido': pedido.id,
            'cliente': pedido.usuario.username,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'bairro': endereco.bairro,
            'lat': endereco.lat_destino, # Pega do modelo Endereco
            'lon': endereco.lon_destino, # Pega do modelo Endereco
            'apelido': endereco.apelido,
        })
    
    # transforma em json para o javascript ler
    dados_json = json.dumps(lista_para_mapa)

    return render(request, "delivery_man/map.html", context={"dados_json":dados_json, 'TOMTOM_KEY':settings.TOMTOM_KEY,})