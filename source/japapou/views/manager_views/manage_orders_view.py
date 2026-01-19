# Seu_App/views.py (Onde você coloca as views)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test # type: ignore
from japapou.models import Order # Certifique-se de importar o modelo Order

# --- Função de Teste para Restringir o Acesso ---
# Se você tiver um campo 'is_staff' no usuário ou um 'tipo_usuario'
# que indique que ele é gerente/admin, use user_passes_test.
# Exemplo assumindo que apenas 'is_staff' pode ver essa página:
#def is_manager(user):
    #return user.is_staff

@login_required
def manage_orders_view(request):
    """
    Exibe uma lista de todos os pedidos, ordenados do mais recente
    para o mais antigo. Ideal para a página de gerenciamento/administração.
    """
    
    # 1. Busca todos os pedidos
    # 2. Ordena por 'created_at' (ou 'date') em ordem decrescente (-)
    
    pedidos = Order.objects.all().order_by('-created_at')

    #print(pedidos)

    contexto = {
        'pedidos': pedidos
    }
    
    # Garanta que o caminho do template esteja correto
    return render(request, 'manager/manage_orders.html', contexto)