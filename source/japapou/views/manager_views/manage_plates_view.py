from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from japapou.models import Plate
from django.urls import reverse
from japapou.forms import PlatesForms
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required


@permission_required('japapou.view_plate', login_url='home')
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

@permission_required('japapou.add_plate', login_url='home')
def create_plates_view(request):
    redirect_to_url_name = request.POST.get('next_redirect_url_name', 'manager_plates')

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
                # CORREÇÃO: Usa a variável obtida do POST para redirecionar
                return redirect(reverse(redirect_to_url_name))
            else:
                for error_field, error_messages in form.errors.items():
                    for message in error_messages:
                        messages.error(request, f"Erro no campo '{error_field}': {message}")
                
                # CORREÇÃO: Redireciona de volta para a página de origem, mesmo com erros
                return redirect(reverse(redirect_to_url_name))
    
    # Se a requisição não for POST ou não houver 'btn-create-plate' no POST
    # ou se for um acesso GET direto, redireciona para a página principal de pratos.
    return redirect(reverse("manager_plates"))

@permission_required('japapou.view_plate', login_url='home')
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
        
        return JsonResponse(request, {'erro': 'Produto não encontrado'}, status=404)
    

permission_required('japapou.change_plate', login_url='home')
def plate_update_view(request, id):
    redirect_to_url_name = request.POST.get('next_redirect_url_name', 'manager_plates')

    if request.method in 'POST':
        
        plate_instance = get_object_or_404(Plate, pk=id)
        form = PlatesForms(request.POST, request.FILES, instance=plate_instance)
        print(request.resolver_match.url_name)

        if form.is_valid():
            form.save()
            messages.success(request, "Prato atualizado com sucesso.")
            return redirect(reverse(redirect_to_url_name))
            
        else:
            for error_field, error_messages in form.errors.items():
                for message in error_messages:
                    messages.error(request, f"Erro no campo '{error_field}': {message}")

    
    return render(request, "manager_plates.html")


permission_required('japapou.delete_plate', login_url='home')
def plate_delete_view(request, id):

    if request.method == "POST":
        plate = get_object_or_404(Plate, pk=id)
        plate_name = plate.name

        if plate.photo:
            plate.photo.delete(save=False)

        plate.delete()
        messages.success(request, f"Prato '{plate_name}' foi excluído com sucesso.")
    
    return redirect("manager_plates")