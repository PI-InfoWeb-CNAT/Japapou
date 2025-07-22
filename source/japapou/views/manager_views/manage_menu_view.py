from django.shortcuts import render  # type: ignore
from japapou.models import Menu, Plate
from django import forms  # type: ignore


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

    plates = Plate.objects.filter(menu=selected_menu)

    context = {
        "select_menu": search,
        "selected": selected_menu,
        "menus": menus,
        "plates": plates,
    }

    return render(
        request,
        template_name="manager/manage_menu.html",
        status=200,
        context=context,
    )
