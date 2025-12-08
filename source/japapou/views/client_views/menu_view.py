from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period, PlateReview
from django.contrib import messages
from datetime import date
from django.db.models import Avg, Q # Importa Q para filtros OR
from django.db.models.functions import Round
from decimal import Decimal, InvalidOperation # Para lidar com valores monetários
import re # Para extrair faixas de preço (ex: "20-50")


@login_required
def client_menu_view(request):
    if request.user.tipo_usuario != 'CLIENT':
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('home')

    # 1. Inicialização de variáveis
    selected_menu = None
    menu_plates = Plate.objects.none() # Queryset vazio por padrão
    today = date.today()
    
    # NEW: Pega o termo de busca da URL
    search_query = request.GET.get('q', '').strip()
    
    # 2. Encontra o período e menu ativo
    periodo_ativo = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()

    if periodo_ativo:
        selected_menu = periodo_ativo.menu
        # Queryset base: todos os pratos do menu ativo
        menu_plates_base = selected_menu.plates.all()
    else:
        messages.warning(request, "De momento, não existe um menu ativo para a data de hoje.")
        
        # Lógica de fallback (Se a intenção era buscar o último menu, isso precisa de mais contexto)
        # Mantendo a lógica original para encontrar um menu se houver um.
        periodos = Period.objects.all()
        for periodo in periodos:
            if periodo.start_date <= date.today() and periodo.end_date >= date.today():
                selected_menu = periodo.menu
        
        if selected_menu:
            menu_plates_base = Plate.objects.filter(menu=selected_menu)
        else:
            menu_plates_base = Plate.objects.none()

    # 3. Aplica a lógica de pesquisa se houver um termo (e um menu base)
    if search_query and menu_plates_base:
        filter_conditions = Q()
        
        # A. Filtra por nome e descrição (case-insensitive)
        filter_conditions |= (
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
        # B. Tenta filtrar por preço/faixa de preço
        try:
            # Expressão regular para encontrar faixa de preço (Ex: 20-50 ou 10.50-30)
            range_match = re.match(r'^\s*(\d+(\.\d{1,2})?)\s*-\s*(\d+(\.\d{1,2})?)\s*$', search_query)
            
            if range_match:
                # Se for uma faixa de preço
                price_min = Decimal(range_match.group(1))
                price_max = Decimal(range_match.group(3))
                
                # Adiciona a condição de faixa de preço (preço entre min e max)
                filter_conditions |= Q(price__gte=price_min) & Q(price__lte=price_max)

            else:
                # Tenta converter para um preço exato. Trata vírgulas como separador decimal.
                exact_price_str = search_query.replace(',', '.')
                exact_price = Decimal(exact_price_str)
                
                # Adiciona a condição de preço exato
                filter_conditions |= Q(price=exact_price)

        except InvalidOperation:
            # O termo de busca não é um número ou faixa de preço válido
            pass
        except Exception as e:
            # Loga qualquer outro erro, mas não interrompe o filtro por nome/descrição
            print(f"Erro ao processar termo de preço: {e}")
            pass

        # Aplica todas as condições (usando OR) ao queryset base
        menu_plates = menu_plates_base.filter(filter_conditions).distinct()
    else:
        # Se não houver busca, usa o queryset base completo
        menu_plates = menu_plates_base

    # 4. Lógica para calcular e aplicar a média de avaliação (media)
    if menu_plates.exists():
        # Filtra as avaliações apenas para os pratos que estão sendo exibidos
        avaliacoes = PlateReview.objects.filter(plate__in=menu_plates.values('pk')).values('plate__name').annotate(media=Round(Avg('value')))
        avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
        
        for plate in menu_plates:
            plate.media = avaliacoes_dict.get(plate.name)
    
    # 5. Prepara o contexto
    context = {
        "selected": selected_menu,
        "menu_plates": menu_plates,
        "search_query": search_query, # Passa o termo de busca para o template para preencher o campo
    }

    return render(request, 'client/menu.html', context)