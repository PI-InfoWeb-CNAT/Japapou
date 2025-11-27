from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period, PlateReview
from django import forms  # type: ignore
from datetime import date
from django.db.models import Avg # type: ignore
from django.db.models.functions import Round # type: ignore
from django.urls import reverse # type: ignore
from japapou.forms import PlatesForms, MenuForms, AddPlatesToMenuForm
from django.contrib import messages # type: ignore
from japapou.views.manager_views import manage_period_view
from django.contrib.auth.decorators import permission_required, login_required # type: ignore
from django.http import JsonResponse


class Search(forms.Form):
    field = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        label=""
    )


@login_required
@permission_required('japapou.view_menu', login_url='home')
def manager_menu_view(request):
    if request.user.tipo_usuario != 'MANAGER':
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('home')

    add_plates_form = AddPlatesToMenuForm()
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

        # Calculamos as avaliações 
        avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
        
        # Convertemos para dicionário para ser mais fácil de usar
        avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}
        
        # Adicionamos a média a cada prato
        for plate in menu_plates:
            plate.media = avaliacoes_dict.get(plate.name)  # Retorna None se não houver avaliação

    else:
        # Se não houver menu ativo, podemos avisar o utilizador
        messages.warning(request, "De momento, não existe um menu ativo para a data de hoje.")

    periodos = Period.objects.all()

    for periodo in periodos:
        if periodo.start_date <= date.today() and periodo.end_date >= date.today():
            selected_menu = periodo.menu

    menu_plates = Plate.objects.filter(menu=selected_menu)

    menus = Menu.objects.all()
    choices = [(menu.name, menu.name) for menu in menus]

    search = Search(request.GET)
    search.fields["field"].choices = choices

    selected_menu = menus.first()

    if search.is_valid():
        selected_menu_name = search.cleaned_data["field"]
        if menus.filter(name=selected_menu_name).exists():
            selected_menu = menus.get(name=selected_menu_name)

    period_choices = []
    if selected_menu:
        periods_for_menu = Period.objects.filter(menu=selected_menu)
        period_choices = [(str(period.id), f"{period.start_date.strftime('%d/%m/%Y')} - {period.end_date.strftime('%d/%m/%Y')}") for period in periods_for_menu]
        

    period_choices.insert(0, ('', 'Todos os Períodos'))

    get_data = request.GET.copy()

    selected_period_id = get_data.get('period_field')

    valid_period_ids = [value for value, label in period_choices]

    if selected_period_id and selected_period_id not in valid_period_ids:
        # Se o valor não é válido para o novo menu, remova-o de get_data
        get_data['period_field'] = '' # Defina como vazio para selecionar "Todos os Períodos"

    search_period_form = manage_period_view.SearchPeriods(get_data)
    search_period_form.fields["period_field"].choices = period_choices

    search_period_form.fields["period_field"].label = ""

    menu_plates = Plate.objects.filter(menu=selected_menu)
    other_plates = Plate.objects.exclude(menu=selected_menu) # pratos que não estáo inseridos no menu atual.

    add_plates_form = AddPlatesToMenuForm(menu=selected_menu, initial={'menu_id': selected_menu.id}) # initial para passar o id do menu para a classe

    avaliacoes = PlateReview.objects.values('plate__name').annotate(media=Round(Avg('value')))
    avaliacoes_dict = {a['plate__name']: a['media'] for a in avaliacoes}

    # Aplicamos a média aos pratos DENTRO do menu
    for plate in menu_plates:
        plate.media = avaliacoes_dict.get(plate.name)

    # Aplicamos a média aos pratos FORA do menu
    for plate in other_plates:
        plate.media = avaliacoes_dict.get(plate.name)

    context = {
        "select_menu": search,
        "selected": selected_menu,
        "menus": menus,
        "menu_plates": menu_plates,
        "other_plates": other_plates,
        "form": PlatesForms(),
        "form_menu": MenuForms(request=request),
        "search_period": search_period_form,
        "avaliacoes": avaliacoes,
        "add_plates_form": add_plates_form,
        
    }
    
    return render(
        request,
        template_name="manager/manage_menu.html",
        status=200,
        context=context,
    )

@login_required
@permission_required('japapou.add_menu', login_url='home')
def create_menu_view(request):
    if request.method == "POST":
        
        form_menu = MenuForms(request.POST, request=request)

        
        if 'btn-create-menu' in request.POST:
            if form_menu.is_valid():
                #form_menu.save(commit=False)
                new_menu = form_menu.save()
                
                messages.success(request, "Menu criado com sucesso.")
                redirect_url = reverse("manager_menu")
                return redirect(f"{redirect_url}?field={new_menu.name}")
            else:
                messages.error(request, "Erro ao criar o menu.")
                return redirect("manager_menu")
        
        return redirect("manager_menu")

    else:
        form_menu = MenuForms(request=request)

@login_required
@permission_required('japapou.change_menu', login_url='home') 
def add_plates_to_menu_view(request):
    """
    Processa a adição de pratos existentes a um menu.
    """
    if request.user.tipo_usuario != 'MANAGER':
        messages.error(request, "Você não tem permissão para realizar essa ação.")
        return redirect('home')

    if request.method == "POST":

        # O menu_id e a lista de plates_to_add vêm do POST
        menu_id = request.POST.get('menu_id') 
        plates_to_add_ids = request.POST.getlist('plates_to_add') # getlist para campos ModelMultipleChoiceField

        if not menu_id:
            messages.error(request, "Erro: O ID do menu não foi fornecido.")
            return redirect("manager_menu")

        try:
            menu = Menu.objects.get(pk=menu_id) 
        except Menu.DoesNotExist:
            messages.error(request, "Menu não encontrado.")
            return redirect("manager_menu")
        
        if plates_to_add_ids:
            # Obtém os objetos Plate com os IDs
            plates = Plate.objects.filter(pk__in=plates_to_add_ids)
            
            # Adiciona os pratos ao campo ManyToMany do menu
            menu.plates.add(*plates) #
            
            messages.success(request, f"Pratos adicionados ao menu '{menu.name}' com sucesso.")
            
        else:
            messages.warning(request, "Nenhum prato selecionado.")
        
        # Redireciona de volta para a view do gerente, mantendo o menu selecionado
        redirect_url = reverse("manager_menu")
        return redirect(f"{redirect_url}?field={menu.name}")
        
    return redirect("manager_menu")


@login_required
@permission_required('japapou.change_menu', login_url='home')
def remove_plate_from_menu_view(request):
    """
    Remove um prato de um menu específico sem excluí-lo do sistema (via AJAX).
    """
    if request.user.tipo_usuario != 'MANAGER':
        return JsonResponse({"success": False, "message": "Permissão negada."}, status=403)
    
    if request.method == "POST":
        
        # O Django precisa de um token CSRF para POST, mesmo via Fetch API
       

        menu_id = request.POST.get('menu_id')
        plate_id = request.POST.get('plate_id')
        
        if not menu_id or not plate_id:
            return JsonResponse({"success": False, "message": "Menu ou Prato não especificado."}, status=400)
            
        try:
            menu = Menu.objects.get(pk=menu_id)
            plate = Plate.objects.get(pk=plate_id)
        except (Menu.DoesNotExist, Plate.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Menu ou Prato inválido."}, status=404)
        
        # 1. REMOÇÃO DO PRATO DO MENU
        menu.plates.remove(plate)
        
        # 2. RETORNO DE SUCESSO
        return JsonResponse({"success": True, "message": f"Prato '{plate.name}' removido do menu '{menu.name}'."})
        
    return JsonResponse({"success": False, "message": "Método não permitido."}, status=445)

@login_required
@permission_required('japapou.change_menu', login_url='home')
def add_single_plate_to_menu_view(request):
    """
    Processa a adição de UM ÚNICO prato existente a um menu (via AJAX/Fetch).
    Esta view retorna JsonResponse.
    """
    if request.user.tipo_usuario != 'MANAGER':
        return JsonResponse({"success": False, "message": "Permissão negada."}, status=403)

    if request.method == "POST":

        # O JavaScript envia plate_id (como 'plates_to_add') e menu_id
        menu_id = request.POST.get('menu_id')
        plate_id = request.POST.get('plates_to_add') # Nome do campo usado no JS

        if not menu_id or not plate_id:
            return JsonResponse({"success": False, "message": "Menu ou Prato não especificado."}, status=400)

        try:
            menu = Menu.objects.get(pk=menu_id)
            plate = Plate.objects.get(pk=plate_id)
        except (Menu.DoesNotExist, Plate.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Menu ou Prato inválido."}, status=404)

        # 1. ADICIONA O PRATO AO CAMPO ManyToMany
        menu.plates.add(plate)

        # 2. RETORNA UM JSON DE SUCESSO (Status 200 OK)
        return JsonResponse({"success": True, "message": f"Prato '{plate.name}' adicionado ao menu '{menu.name}'."})

    return JsonResponse({"success": False, "message": "Método não permitido."}, status=445)