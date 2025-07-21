from django.shortcuts import render  # type: ignore
from japapou.models.prato import Prato

def manager_menu_view(request):
    pratos = Prato.objects.all()
    
    context = {
        "pratos": pratos
    }

    return render(request, template_name="manager/manage_menu.html", status=200, context=context)
