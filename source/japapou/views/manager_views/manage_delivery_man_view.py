from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from japapou.models import CustomUser
from japapou.forms import DeliveryRegisterForm
import logging

logger = logging.getLogger(__name__)

def validate_manager_access(user):
    """Validação customizada para acesso do gerente"""
    return user.tipo_usuario == 'MANAGER'


@login_required
@permission_required('japapou.view_customuser', login_url='home')
@user_passes_test(validate_manager_access, login_url='home')
def manager_delivery_man_view(request):
    """Lista todos os entregadores"""
    delivery_men = CustomUser.objects.filter(
        tipo_usuario='DELIVERY_MAN'
    ).order_by('-date_joined')

    return render(request, "manager/manage_delivery_man.html", {
        "delivery_men": delivery_men
    })



@login_required
@permission_required('japapou.add_customuser', login_url='home')
@user_passes_test(validate_manager_access, login_url='home')
@csrf_protect
def manager_delivery_man_create_view(request):
    """Cria um novo entregador"""
    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                delivery_man = form.save(commit=False)
                delivery_man.tipo_usuario = 'DELIVERY_MAN'

                # ✅ Garante que a senha será criptografada
                raw_password = form.cleaned_data.get("password")
                if raw_password:
                    delivery_man.set_password(raw_password)

                delivery_man.save()

                logger.info(f"Delivery man {delivery_man.username} created by {request.user}")
                messages.success(request, "Entregador registrado com sucesso!")
                return redirect('manager_delivery_man')

            except Exception as e:
                logger.error(f"Error creating delivery man: {str(e)}")
                messages.error(request, f"Erro ao criar entregador: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DeliveryRegisterForm()

    return render(request, "manager/manage_delivery_man_form.html", {"form": form})



@login_required
@permission_required('japapou.view_customuser', login_url='home')
@user_passes_test(validate_manager_access, login_url='home')
def manager_delivery_man_detail_view(request, id):
    """Exibe os detalhes de um entregador"""
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    return render(request, "manager/manage_delivery_man_detail.html", {
        "delivery_man": delivery_man
    })


@login_required
@permission_required('japapou.change_customuser', login_url='home')
@user_passes_test(validate_manager_access, login_url='home')
@csrf_protect
def manager_delivery_man_update_view(request, id):
    """
    Atualiza os dados de um entregador (sem exigir senha obrigatória)
    """
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES, instance=delivery_man)
        if form.is_valid():
            try:
                delivery_man = form.save(commit=False)
                delivery_man.tipo_usuario = 'DELIVERY_MAN'

                # ✅ Só atualiza senha se o campo não estiver vazio
                raw_password = form.cleaned_data.get("password")
                if raw_password:
                    delivery_man.set_password(raw_password)

                delivery_man.save()

                logger.info(f"Delivery man {delivery_man.username} updated by {request.user}")
                messages.success(request, "Entregador atualizado com sucesso!")
                return redirect('manager_delivery_man')

            except Exception as e:
                logger.error(f"Error updating delivery man {id}: {str(e)}")
                messages.error(request, f"Erro ao atualizar entregador: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DeliveryRegisterForm(instance=delivery_man)

    return render(request, "manager/manage_delivery_man_edit.html", {
        "form": form,
        "delivery_man": delivery_man
    })



@login_required
@permission_required('japapou.delete_customuser', login_url='home')
@user_passes_test(validate_manager_access, login_url='home')
@csrf_protect
def manager_delivery_man_delete_view(request, id):
    """Exclui um entregador"""
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        try:
            delivery_man_name = delivery_man.username
            delivery_man.delete()
            logger.info(f"Delivery man {delivery_man_name} deleted by {request.user}")
            messages.success(request, f"Entregador {delivery_man_name} excluído com sucesso!")
        except Exception as e:
            logger.error(f"Error deleting delivery man {id}: {str(e)}")
            messages.error(request, f"Erro ao excluir entregador: {str(e)}")

    return redirect('manager_delivery_man')

