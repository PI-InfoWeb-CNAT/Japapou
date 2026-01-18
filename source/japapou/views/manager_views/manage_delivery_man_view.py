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
from japapou.models import CustomUser, CourierReview
from japapou.forms import DeliveryRegisterForm 
from datetime import date
import re
from django.db.models import Avg # type: ignore
from django.db.models.functions import Round # type: ignore


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
    """Cria um novo entregador com validações e exibe erros no formulário"""
    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_man = form.save(commit=False)
            delivery_man.tipo_usuario = 'DELIVERY_MAN'

            
            birth_date = form.cleaned_data.get('data_nascimento')
            if birth_date:
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    form.add_error('data_nascimento', 'O entregador deve ter pelo menos 18 anos de idade.')

            cpf = form.cleaned_data.get('cpf', '')
            cpf_numbers = re.sub(r'\D', '', cpf)
            if len(cpf_numbers) != 11:
                form.add_error('cpf', 'CPF inválido. Deve conter 11 números.')
            delivery_man.cpf = cpf_numbers

            telefone = form.cleaned_data.get('telefone', '').strip()
            telefone_numbers = re.sub(r'\D', '', telefone)  

            if not telefone_numbers:
                form.add_error('telefone', 'Telefone obrigatório.')
            elif len(telefone_numbers) < 10 or len(telefone_numbers) > 11:
                form.add_error('telefone', 'Telefone inválido. Deve conter 10 ou 11 números.')
            else:
                delivery_man.telefone = telefone_numbers

            placa = form.cleaned_data.get('placa_moto', '').upper().replace('-', '')
            if placa and not re.match(r'^[A-Z]{3}[0-9]{4}$', placa):
                form.add_error('placa_moto', 'Placa inválida. Deve estar no formato ABC-1234.')
            delivery_man.placa_moto = f"{placa[:3]}-{placa[3:]}" if placa else ''

            if form.errors:
                return render(request, "manager/manager_delivery_man_register.html", {"form": form})

            raw_password = form.cleaned_data.get("password")
            if raw_password:
                delivery_man.set_password(raw_password)
            else:
                form.add_error('password', 'Senha obrigatória.')
                return render(request, "manager/manager_delivery_man_register.html", {"form": form})

            delivery_man.save()
            form.save_m2m()
            messages.success(request, "Entregador registrado com sucesso!")
            return redirect('manager_delivery_man')

        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = DeliveryRegisterForm()

    return render(request, "manager/manager_delivery_man_register.html", {"form": form})

@manager_required('japapou.view_customuser')
def manage_delivery_man_view(request):
    """Lista todos os entregadores"""

    avaliacoes_dict = {}

    try:
        delivery_men = CustomUser.objects.filter(
            tipo_usuario='DELIVERY_MAN',
            is_active=True  
        ).order_by('-date_joined')

        courier_reviews = CourierReview.objects.values('entregador__username').annotate(
                            media=Round(Avg('value'))
                            )
        
        avaliacoes_dict = {a['entregador__username']: a['media'] for a in courier_reviews}
        
        for de in delivery_men:
            de.media = avaliacoes_dict.get(de.username)
        

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
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    return render(request, "manager/manager_delivery_man_detail.html", {
        "delivery_man": delivery_man
    })




@manager_required('japapou.change_customuser')
@csrf_protect
def manager_delivery_man_update_view(request, id):
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    initial_password = delivery_man.password  # Mantém a senha atual se não for alterada

    if request.method == "POST":
        form = DeliveryRegisterForm(request.POST, request.FILES, instance=delivery_man)
        
        if form.is_valid():
            delivery_man = form.save(commit=False)
            delivery_man.tipo_usuario = 'DELIVERY_MAN'

            birth_date = form.cleaned_data.get('data_nascimento')
            if birth_date:
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    form.add_error('data_nascimento', 'O entregador deve ter pelo menos 18 anos de idade.')

            
            cpf = re.sub(r'\D', '', form.cleaned_data.get('cpf', ''))
            if len(cpf) != 11:
                form.add_error('cpf', 'CPF inválido. Deve conter 11 números.')
            delivery_man.cpf = cpf

            telefone_numbers = re.sub(r'\D', '', form.cleaned_data.get('telefone', ''))
            if not telefone_numbers:
                form.add_error('telefone', 'Telefone obrigatório.')
            elif len(telefone_numbers) < 10 or len(telefone_numbers) > 11:
                form.add_error('telefone', 'Telefone inválido. Deve conter 10 ou 11 números.')
            else:
                delivery_man.telefone = telefone_numbers

            placa = form.cleaned_data.get('placa_moto', '').upper().replace('-', '')
            if placa and not re.match(r'^[A-Z]{3}[0-9]{4}$', placa):
                form.add_error('placa_moto', 'Placa inválida. Deve estar no formato ABC-1234.')
            delivery_man.placa_moto = f"{placa[:3]}-{placa[3:]}" if placa else ''

            raw_password = form.cleaned_data.get('password')
            if raw_password:
                delivery_man.set_password(raw_password)
            else:
                delivery_man.password = initial_password

            if form.errors:
                return render(request, "manager/manager_delivery_man_edit.html", {
                    "form": form,
                    "delivery_man": delivery_man
                })

            delivery_man.save()
            form.save_m2m()
            messages.success(request, "Entregador atualizado com sucesso!")
            return redirect('manager_delivery_man')
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
    """Exclui um entregador"""
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