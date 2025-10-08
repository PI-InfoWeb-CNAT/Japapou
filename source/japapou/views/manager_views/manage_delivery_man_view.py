from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from japapou.models import CustomUser
from japapou.forms import DeliveyrRegisterForm
from django.urls import reverse
from django.http import JsonResponse


@login_required
@permission_required('japapou.view_customuser', login_url='home')
def manager_manage_delivery_man_view(request):
    # Apenas gerente pode acessar
    if request.user.tipo_usuario != 'MANAGER':
        return render(request, "404.html", status=404)

    entregadores = CustomUser.objects.filter(tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        form = DeliveyrRegisterForm(request.POST)
        if form.is_valid():
            delivery_user = form.save(commit=False)
            delivery_user.tipo_usuario = 'DELIVERY_MAN'
            delivery_user.set_password(form.cleaned_data["password"])  # criptografa a senha
            delivery_user.save()
            messages.success(request, "Entregador cadastrado com sucesso.")
            return redirect('manager_manage_delivery_man')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro em {field}: {error}")
    else:
        form = DeliveyrRegisterForm()

    context = {
        "entregadores": entregadores,
        "form": form
    }

    return render(request, "manager/manage_delivery_man.html", context)


@login_required
@permission_required('japapou.change_customuser', login_url='home')
def delivery_man_update_view(request, id):
    entregador = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        form = DeliveyrRegisterForm(request.POST, instance=entregador)
        if form.is_valid():
            delivery_user = form.save(commit=False)
            delivery_user.tipo_usuario = 'DELIVERY_MAN'
            if form.cleaned_data.get("password"):
                delivery_user.set_password(form.cleaned_data["password"])
            delivery_user.save()
            messages.success(request, "Entregador atualizado com sucesso.")
            return redirect('manager_manage_delivery_man')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro em {field}: {error}")
    else:
        form = DeliveyrRegisterForm(instance=entregador)

    return render(request, "manager/manage_delivery_man_edit.html", {"form": form, "entregador": entregador})


@login_required
@permission_required('japapou.delete_customuser', login_url='home')
def delivery_man_delete_view(request, id):
    entregador = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    if request.method == "POST":
        entregador.delete()
        messages.success(request, "Entregador excluído com sucesso.")
    return redirect('manager_manage_delivery_man')


@login_required
@permission_required('japapou.view_customuser', login_url='home')
def delivery_man_get_json(request, id):
    try:
        entregador = CustomUser.objects.get(pk=id, tipo_usuario='DELIVERY_MAN')
        data = {
            "id": entregador.id,
            "username": entregador.username,
            "email": entregador.email,
            "telefone": entregador.telefone,
            "cpf": entregador.cpf,
            "modelo_moto": entregador.modelo_moto,
            "cor_moto": entregador.cor_moto,
            "Placa_moto": entregador.Placa_moto,
            "cnh": entregador.cnh,
        }
        return JsonResponse(data)
    except CustomUser.DoesNotExist:
        return JsonResponse({"erro": "Entregador não encontrado"}, status=404)

