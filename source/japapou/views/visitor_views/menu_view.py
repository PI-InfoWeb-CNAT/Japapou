from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period, PlateReview
from django.contrib import messages
from datetime import date
from django.db.models import Avg
from django.db.models.functions import Round


# pôr uma parte pra pegar a avaliação quando ela for feita 
# pegar e retornar um valor inteiro
# mudar o js pra fazer as estrelas aparecerem e desaparecerem, ok?
# o css ainda é o do manager (mudar para o do cliente)


from django.shortcuts import render 
from japapou.models import Menu, Plate, Period, PlateReview
from django.contrib import messages
from datetime import date
from django.db.models import Avg
from django.db.models.functions import Round


def visitor_menu_view(request):
    # Inicializa as variáveis com valores seguros
    selected_menu = None
    menu_plates = Plate.objects.none() # Inicializa como QuerySet vazia
    avaliacoes_dict = {}
    today = date.today()

    # 1. Encontra o período ativo
    periodo_ativo = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()

    if periodo_ativo:
        selected_menu = periodo_ativo.menu
        menu_plates = selected_menu.plates.all()

        # 2. Lógica de Avaliação (Só executa se houver um menu)
        # Calcula as médias das avaliações (Round(Avg('value')) arredonda para inteiro)
        avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
        
        # Converte para dicionário para acesso rápido
        avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
        
        # Adiciona a média a cada prato
        for plate in menu_plates:
            # plate.media será o valor da média ou None (se não houver avaliação)
            plate.media = avaliacoes_dict.get(plate.name) 
    
    else:
        # Se não houver menu ativo, avisa o usuário (melhor prática)
        messages.info(request, "De momento, não existe um menu ativo para a data de hoje.")
        
    # O `menu_plates` (e as avaliações) do bloco 'if' agora são as que prevalecem.
    
    # Prepara o contexto
    context = {
        "selected": selected_menu,
        "menu_plates": menu_plates, # Será uma QuerySet com pratos ou uma QuerySet vazia (Plate.objects.none())
    }
    
    return render(request, template_name="visitor/menu.html", context=context, status=200)


'''

select avg(value) 
from PlateReview pr
inner join Plate p on p.id = pr.plate_id


PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))


'''
