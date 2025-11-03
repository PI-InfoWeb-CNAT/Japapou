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



@login_required
def client_menu_view(request):
    if request.user.tipo_usuario != 'CLIENT':
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('home')
    
    selected_menu = None
    menu_plates = [] 
    avaliacoes_dict = {}
    today = date.today()

    periodo_ativo = Period.objects.filter(start_date__lte=today, end_date__gte=today).first()

    if periodo_ativo:
        # Se encontrámos, definimos o menu
        selected_menu = periodo_ativo.menu
        
        # E buscamos os pratos DESSE menu
        menu_plates = selected_menu.plates.all()

        # Calculamos as avaliações (o seu código já estava ótimo aqui)
        avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
        
        # Convertemos para dicionário para ser mais fácil de usar
        avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
        
        # Adicionamos a média a cada prato
        for plate in menu_plates:
            plate.media = avaliacoes_dict.get(plate.name)  # Retorna None se não houver avaliação

    else:
        # 4. (Opcional) Se não houver menu ativo, podemos avisar o utilizador
        messages.warning(request, "De momento, não existe um menu ativo para a data de hoje.")

    periodos = Period.objects.all()

    for periodo in periodos:
        if periodo.start_date <= date.today() and periodo.end_date >= date.today():
            selected_menu = periodo.menu

    menu_plates = Plate.objects.filter(menu=selected_menu)

    avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
    # avaliacoes = PlateReview.objects.all()
    print(avaliacoes)

    
    avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
    for plate in menu_plates:
        plate.media = avaliacoes_dict.get(plate.name)  # None se não tiver


    context = {
        "selected": selected_menu,
        "menu_plates": menu_plates,
        "avaliacoes": avaliacoes,
    }
    
    return render(request, template_name="client/menu.html", context=context, status=200)


'''

select avg(value) 
from PlateReview pr
inner join Plate p on p.id = pr.plate_id


PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))


'''
