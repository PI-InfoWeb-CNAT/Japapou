from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.models import Order # Importar modelos necessários
from django.conf import settings
import json

@login_required
@permission_required('japapou.view_order', login_url='login')
def delivery_man_orders_view(request):
    """
    Lista os pedidos pendentes atribuídos ao entregador logado e prepara 
    os dados de geolocalização (JSON) para exibição em mapa interativo.
    """
    
    # --- Verificação de Segurança ---
    # Garante que apenas usuários do tipo 'DELIVERY_MAN' acessem esta página.
    # Se for outro tipo, redireciona para a home.
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    # --- Consulta ao Banco de Dados ---
    # 1. Filtra pedidos onde o entregador é o usuário atual.
    # 2. Ordena do mais recente para o mais antigo.
    # 3. prefetch_related: Otimização importante! Já carrega os itens e pratos associados 
    #    numa única consulta, evitando lentidão (N+1 queries) no template HTML.
    pedidos_pendentes = Order.objects.filter(entregador_id=request.user.id, status='A_CAMINHO').order_by('-created_at').prefetch_related('itens__prato')
    
    # Print para depuração no terminal (útil para o desenvolvedor verificar se a busca funcionou)
    print(f"Pedidos pendentes encontrados: {pedidos_pendentes.count()}")

    # --- Preparação de Dados para o Mapa (JavaScript) ---
    lista_para_mapa = []

    for pedido in pedidos_pendentes:
        # Só adicionamos ao mapa se:
        # 1. O pedido estiver com status 'A_CAMINHO'.
        # 2. For um pedido de ENTREGA.
        # 3. Tiver um objeto de endereço vinculado e ambos lat/lon presentes.
        if (pedido.status == 'A_CAMINHO' and
            pedido.tipo_pedido == 'ENTREGA' and
            pedido.endereco_entrega and
            pedido.endereco_entrega.lat_destino is not None and
            pedido.endereco_entrega.lon_destino is not None):

            endereco = pedido.endereco_entrega

            # Cria um dicionário simples apenas com os dados necessários para o mapa
            lista_para_mapa.append({
                'id': pedido.id,
                'cliente': pedido.usuario.username,
                'lat': float(endereco.lat_destino),
                'lon': float(endereco.lon_destino),
                'endereco': f"{endereco.logradouro}, {endereco.numero}, {endereco.bairro}",
            })

    # Converte a lista de dicionários Python para uma String JSON.
    # Isso é essencial para que o JavaScript no navegador consiga ler a variável 'mapa_json'.
    mapa_json = json.dumps(lista_para_mapa)
    print("Mapa JSON enviado ao template:", mapa_json)

    # --- Renderização ---
    return render(request, template_name="delivery_man/orders.html", context={
        'pedidos': pedidos_pendentes,  # Objeto QuerySet (para a lista HTML)
        'mapa_json': mapa_json,        # String JSON (para o script do Mapa)
        'TOMTOM_KEY': settings.TOMTOM_KEY # Chave da API de mapas (vinda do settings.py)
    }, status=200)



