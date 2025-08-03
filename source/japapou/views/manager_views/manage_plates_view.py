from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from japapou.models import Plate
from django.urls import reverse
from japapou.forms import PlatesForms
from django.contrib import messages
from django.http import JsonResponse

def manager_plates_view(request):
    plates = Plate.objects.all()

    if request.method == "POST":
        form = PlatesForms(request.POST, request.FILES)
        if 'btn-create-plate' in request.POST:
            if form.is_valid():
                plate_instance = form.save(commit=False)
                plate_instance.save()
                selected_menus = form.cleaned_data.get("menus")

                if selected_menus:
                    for menu_obj in selected_menus:
                        menu_obj.plates.add(plate_instance)

                messages.success(request, "Prato adicionado com sucesso.")
                return reverse("manager_plates")
    
    else:
        form = PlatesForms(request.POST, request.FILES)

    context = {
        "plates": plates,
        "form": form
    }

    return render(
        request,
        template_name="manager/manage_plates.html",
        status=200,
        context=context,
    )

def plate_get_json(request, id):
    
    try:
        plate = Plate.objects.get(pk=id)

        data = {
            "id": plate.id,
            "name": plate.name,
            "description": plate.description,
            "price": plate.price,
            'photo_url': plate.photo.url if plate.photo else None,
            'menus': list(plate.menu_set.values_list('id', flat=True))
        }

        return JsonResponse(data)

    except Plate.DoesNotExist:
        
        return JsonResponse({'erro': 'Produto não encontrado'}, status=404)
    

def plate_update_view(request, id):
    # Garante que o método é POST
    if request.method in 'POST':
        # Busca o prato existente no banco de dados ou retorna um erro 404 se não encontrar
        plate_instance = get_object_or_404(Plate, pk=id)
        
        # Cria uma instância do formulário, preenchendo com os dados da requisição (request.POST)
        # e associando ao prato que estamos editando (instance=plate_instance)
        form = PlatesForms(request.POST, request.FILES, instance=plate_instance)
        
        if form.is_valid():
            # Salva o formulário. Como ele está ligado a uma 'instance', o Django fará um UPDATE no banco
            form.save()
            messages.success(request, "Prato atualizado com sucesso.")
        else:
            # Se o formulário for inválido, exibe os erros
            # (Você pode querer tratar isso de forma mais elegante no futuro)
            for error_field, error_messages in form.errors.items():
                for message in error_messages:
                    messages.error(request, f"Erro no campo '{error_field}': {message}")

    # Redireciona o usuário de volta para a página de gerenciamento de pratos
    return redirect("manager_plates")

def plate_delete_view(request, id):

    if request.method == "POST":
        plate = get_object_or_404(Plate, pk=id)
        plate_name = plate.name

        if plate.photo:
            plate.photo.delete(save=False)

        plate.delete()
        messages.success(request, f"Prato '{plate_name}' foi excluído com sucesso.")
    
    return redirect("manager_plates")