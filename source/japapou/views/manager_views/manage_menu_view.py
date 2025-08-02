from django.shortcuts import render, redirect  # type: ignore
from japapou.models import Menu, Plate
from django import forms  # type: ignore
from django.urls import reverse
from japapou.forms import PlatesForms, MenuForms
from django.contrib import messages


class Search(forms.Form):
    field = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"onchange": "submit();"}),
    )


def manager_menu_view(request):
    menus = Menu.objects.all()
    choices = [(menu.name, menu.name) for menu in menus]

    search = Search(request.GET)
    search.fields["field"].choices = choices

    selected_menu = menus.first()

    if search.is_valid():
        selected_menu_name = search.cleaned_data["field"]
        if menus.filter(name=selected_menu_name).exists():
            selected_menu = menus.get(name=selected_menu_name)

    menu_plates = Plate.objects.filter(menu=selected_menu)
    other_plates = Plate.objects.exclude(menu=selected_menu)

    if request.method == "POST":
        form = PlatesForms(request.POST, request.FILES)
        form_menu = MenuForms(request.POST)

        # FORMULARIO PARA CRIAR O NOVO MENU
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
        # FORMULARIO PARA CRIAR O NOVO MENU


        if 'btn-create-plate' in request.POST:
            if form.is_valid():
                plate_instance = form.save(commit=False)
                plate_instance.save()
                selected_menus = form.cleaned_data.get("menus")

                if selected_menus:
                    for menu_obj in selected_menus:
                        menu_obj.plates.add(plate_instance)

                messages.success(request, "Prato adicionado com sucesso.")
                redirect_url = reverse("manager_menu")

        if selected_menu:
            redirect_url += f"?field={selected_menu.name}"
        return redirect(redirect_url)
    
    else:
        form = PlatesForms()
        form_menu = MenuForms()

    context = {
        "select_menu": search,
        "selected": selected_menu,
        "menus": menus,
        "menu_plates": menu_plates,
        "other_plates": other_plates,
        "form": form,
        "form_menu": form_menu,
    }
    
    return render(
        request,
        template_name="manager/manage_menu.html",
        status=200,
        context=context,
    )
