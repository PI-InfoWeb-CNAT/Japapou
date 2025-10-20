from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period
from django.contrib import messages
from datetime import date


# pôr uma parte pra pegar a avaliação quando ela for feita 
# pegar e retornar um valor inteiro
# mudar o js pra fazer as estrelas aparecerem e desaparecerem, ok?
# o css ainda é o do manager (mudar para o do cliente)



@login_required
@permission_required('japapou.view_menu', login_url='login')
def client_menu_view(request):
    if request.user.tipo_usuario != 'CLIENT':
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('home')

    periodos = Period.objects.all()

    for periodo in periodos:
        if periodo.start_date <= date.today() and periodo.end_date >= date.today():
            selected_menu = periodo.menu

    menu_plates = Plate.objects.filter(menu=selected_menu)

    context = {
        "selected": selected_menu,
        "menu_plates": menu_plates,       
    }
    
    return render(request, template_name="client/menu.html", context=context, status=200)

