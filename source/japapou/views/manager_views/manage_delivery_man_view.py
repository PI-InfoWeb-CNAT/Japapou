from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import (
    login_required, 
    permission_required, 
    user_passes_test,
)
from django.views.decorators.csrf import csrf_protect 
from django.contrib import messages
from functools import wraps
import logging
from japapou.models import CustomUser 
from japapou.forms import DeliveryRegisterForm 


logger = logging.getLogger(__name__)

def validate_manager_access(user):
    """Validação customizada para acesso do gerente"""
    return user.tipo_usuario == 'MANAGER'

def manager_required(permission):
    """
    Decorator customizado que combina:
    1. @login_required
    2. @permission_required (com a permissão específica fornecida)
    3. @user_passes_test (validando se é um MANAGER)
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='home')
        @permission_required(permission, login_url='home')
        @user_passes_test(validate_manager_access, login_url='home')
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



@manager_required('japapou.add_customuser')
@csrf_protect  
def manager_delivery_man_create_view(request):
    """Cria um novo entregador"""
    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                delivery_man = form.save(commit=False)
                delivery_man.tipo_usuario = 'DELIVERY_MAN'
                raw_password = form.cleaned_data.get("password")
                if raw_password:
                    delivery_man.set_password(raw_password)
                delivery_man.save()
                form.save_m2m() 
                logger.info(f"Delivery man {delivery_man.username} created by {request.user.username}")
                messages.success(request, "Entregador registrado com sucesso!")
                return redirect('manager_delivery_man')

            except Exception as e:
                logger.error(f"Error creating delivery man: {str(e)}")
                messages.error(request, f"Erro ao criar entregador: {e}")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DeliveryRegisterForm()

    # USE O NOME QUE VOCÊ QUER: manager_delivery_man_register.html
    return render(request, "manager/manager_delivery_man_register.html", {"form": form})


@manager_required('japapou.view_customuser')
def manage_delivery_man_view(request):
    """Lista todos os entregadores"""
    try:
        delivery_men = CustomUser.objects.filter(
            tipo_usuario='DELIVERY_MAN'
        ).order_by('-date_joined')

        # MANTENDO manager_delivery_man.html para listagem
        return render(request, "manager/manager_delivery_man.html", {
            "delivery_men": delivery_men
        })
    except Exception as e:
        logger.error(f"Error listing delivery men: {str(e)}")
        messages.error(request, "Erro ao listar entregadores.")
        return redirect('home')


@manager_required('japapou.view_customuser')
def manager_delivery_man_detail_view(request, id):
    """Exibe os detalhes de um entregador"""
    # Busca o usuário pelo ID e garante que ele é um 'DELIVERY_MAN'
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    return render(request, "manager/manager_delivery_man_detail.html", {
        "delivery_man": delivery_man
    })


@manager_required('japapou.change_customuser')
@csrf_protect
def manager_delivery_man_update_view(request, id):
    """
    Atualiza os dados de um entregador (sem exigir senha obrigatória)
    """
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    
    initial_password = delivery_man.password 

    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES, instance=delivery_man)
        
        if form.is_valid():
            try:
                delivery_man = form.save(commit=False)
                delivery_man.tipo_usuario = 'DELIVERY_MAN' 

                raw_password = form.cleaned_data.get("password")
                if raw_password:
                    delivery_man.set_password(raw_password)
                else:
                    delivery_man.password = initial_password

                delivery_man.save()
                form.save_m2m()
                
                logger.info(f"Delivery man {delivery_man.username} updated by {request.user.username}")
                messages.success(request, "Entregador atualizado com sucesso!")
                return redirect('manager_delivery_man')

            except Exception as e:
                logger.error(f"Error updating delivery man {id}: {str(e)}")
                messages.error(request, f"Erro ao atualizar entregador: {e}")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DeliveryRegisterForm(instance=delivery_man)

    return render(request, "manager/manager_delivery_man_edit.html", {
        "form": form,
        "delivery_man": delivery_man
    })


@manager_required('japapou.delete_customuser')
@csrf_protect
def manager_delivery_man_delete_view(request, id):
    """Exclui um entregador (deve ser chamado por um método POST, geralmente de um formulário)"""
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        try:
            delivery_man_name = delivery_man.username
            delivery_man.delete() 
            
            logger.info(f"Delivery man {delivery_man_name} deleted by {request.user.username}")
            messages.success(request, f"Entregador {delivery_man_name} excluído com sucesso!")
        except Exception as e:
            logger.error(f"Error deleting delivery man {id}: {str(e)}")
            messages.error(request, f"Erro ao excluir entregador: {e}")

    return redirect('manager_delivery_man')