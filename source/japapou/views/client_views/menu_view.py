from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period, PlateReview
from django.contrib import messages
from datetime import date
from django.db.models import Avg
from django.db.models.functions import Round


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
        selected_menu = periodo_ativo.menu
        menu_plates = selected_menu.plates.all()
        avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
        avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
        for plate in menu_plates:
            plate.media = avaliacoes_dict.get(plate.name)  
    else:
        messages.warning(request, "De momento, não existe um menu ativo para a data de hoje.")

    periodos = Period.objects.all()

    for periodo in periodos:
        if periodo.start_date <= date.today() and periodo.end_date >= date.today():
            selected_menu = periodo.menu

    menu_plates = Plate.objects.filter(menu=selected_menu)

    avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
    print(avaliacoes)

    
    avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
    for plate in menu_plates:
        plate.media = avaliacoes_dict.get(plate.name)

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
