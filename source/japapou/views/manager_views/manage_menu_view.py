from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate, Period
from django import forms  # type: ignore
from django.urls import reverse
from japapou.forms import PlatesForms, MenuForms
from django.contrib import messages
from japapou.views.manager_views import manage_period_view
from django.contrib.auth.decorators import permission_required, login_required



class Search(forms.Form):
    field = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        label="Menus"
    )


@login_required
@permission_required('japapou.view_menu', login_url='home')
def manager_menu_view(request):
    if request.user.tipo_usuario != 'GERENTE':
        return redirect('home')


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

    menu_plates = Plate.objects.filter(menu=selected_menu)
    other_plates = Plate.objects.exclude(menu=selected_menu)

    context = {
        "select_menu": search,
        "selected": selected_menu,
        "menus": menus,
        "menu_plates": menu_plates,
        "other_plates": other_plates,
        "form": PlatesForms(),
        "form_menu": MenuForms(),
        "search_period": search_period_form,
        
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
        
        form_menu = MenuForms(request.POST)

        
        if 'btn-create-menu' in request.POST:
            if form_menu.is_valid():
                #form_menu.save(commit=False)
                new_menu = form_menu.save()
                
                messages.success(request, "Menu criado com sucesso.")
                redirect_url = reverse("manager_menu")
                return redirect(f"{redirect_url}?field={new_menu.name}")
            else:
                messages.error(request, "Erro ao criar o menu.")
                redirect_url = reverse("manager_menu")
        
    
    else:
        form_menu = MenuForms()