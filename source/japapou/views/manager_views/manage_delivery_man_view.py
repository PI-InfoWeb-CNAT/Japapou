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
    """
    Processa o cadastro de um novo entregador, executando validações personalizadas 
    (idade, formatação de CPF/telefone, placa) antes de salvar no banco de dados.
    """
    
    # Verifica se o formulário foi enviado (usuário clicou em "Salvar/Cadastrar")
    if request.method == "POST":
        # Preenche o formulário com os dados de texto (POST) e arquivos/fotos (FILES)
        form = DeliveryRegisterForm(request.POST, request.FILES)
        
        # 1. Primeira verificação padrão do Django (tipos de dados, campos obrigatórios básicos)
        if form.is_valid():
            # Cria uma instância do objeto na memória, mas NÃO salva no banco ainda (commit=False).
            # Isso permite modificar os dados antes de gravar definitivamente.
            delivery_man = form.save(commit=False)
            
            # Define manualmente o tipo de usuário para garantir que é um entregador
            delivery_man.tipo_usuario = 'DELIVERY_MAN'

            # --- Validação de Idade ---
            birth_date = form.cleaned_data.get('data_nascimento')
            if birth_date:
                today = date.today()
                # Cálculo preciso da idade levando em conta o mês e dia atual
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    # Se for menor, adiciona um erro específico ao campo 'data_nascimento'
                    form.add_error('data_nascimento', 'O entregador deve ter pelo menos 18 anos de idade.')

            # --- Validação e Limpeza de CPF ---
            cpf = form.cleaned_data.get('cpf', '')
            # Usa Regex para remover tudo que NÃO for dígito (mantém apenas números)
            cpf_numbers = re.sub(r'\D', '', cpf)
            
            if len(cpf_numbers) != 11:
                form.add_error('cpf', 'CPF inválido. Deve conter 11 números.')
            
            # Atualiza o objeto com o CPF limpo (apenas números)
            delivery_man.cpf = cpf_numbers

            # --- Validação e Limpeza de Telefone ---
            telefone = form.cleaned_data.get('telefone', '').strip()
            telefone_numbers = re.sub(r'\D', '', telefone)  

            if not telefone_numbers:
                form.add_error('telefone', 'Telefone obrigatório.')
            elif len(telefone_numbers) < 10 or len(telefone_numbers) > 11:
                form.add_error('telefone', 'Telefone inválido. Deve conter 10 ou 11 números.')
            else:
                delivery_man.telefone = telefone_numbers

            # --- Validação de Placa ---
            # Converte para maiúsculas e remove o traço inicial, se houver
            placa = form.cleaned_data.get('placa_moto', '').upper().replace('-', '')
            
            # Valida se a placa segue o padrão antigo (3 letras e 4 números, ex: ABC1234)
            if placa and not re.match(r'^[A-Z]{3}[0-9]{4}$', placa):
                form.add_error('placa_moto', 'Placa inválida. Deve estar no formato ABC-1234.')
            
            # Se válida, formata visualmente com o traço para salvar no banco
            delivery_man.placa_moto = f"{placa[:3]}-{placa[3:]}" if placa else ''

            # --- Verificação Final de Erros ---
            # Se alguma das validações manuais acima adicionou erros (form.add_error),
            # interrompe o processo e devolve a página com os avisos.
            if form.errors:
                return render(request, "manager/manager_delivery_man_register.html", {"form": form})

            # --- Tratamento de Senha ---
            raw_password = form.cleaned_data.get("password")
            if raw_password:
                # Criptografa a senha (hash) antes de salvar. Nunca salvar senha em texto puro!
                delivery_man.set_password(raw_password)
            else:
                form.add_error('password', 'Senha obrigatória.')
                return render(request, "manager/manager_delivery_man_register.html", {"form": form})

            # 2. Salva o objeto no banco de dados
            delivery_man.save()
            # Salva as relações ManyToMany (necessário quando se usa commit=False)
            form.save_m2m()
            
            # Mensagem de sucesso e redirecionamento
            messages.success(request, "Entregador registrado com sucesso!")
            return redirect('manager_delivery_man')

        else:
            # Caso a validação básica do Django falhe logo no início
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        # Se for uma requisição GET (primeiro acesso à página), cria um formulário vazio
        form = DeliveryRegisterForm()

    # Renderiza o template HTML
    return render(request, "manager/manager_delivery_man_register.html", {"form": form})

@manager_required('japapou.view_customuser')
def manage_delivery_man_view(request):
    """
    Exibe a lista de todos os entregadores ativos, calculando e agregando 
    a média das avaliações (estrelas) recebidas por cada um.
    """

    avaliacoes_dict = {}

    try:
        # Busca todos os usuários que são entregadores e estão marcados como ativos.
        # Ordena do mais recente para o mais antigo ('-date_joined').
        delivery_men = CustomUser.objects.filter(
            tipo_usuario='DELIVERY_MAN',
            is_active=True  
        ).order_by('-date_joined')

        # --- Lógica de Cálculo de Média ---
        # Aqui o Django faz uma consulta agregada (GROUP BY):
        # 1. .values('entregador__username'): Agrupa as avaliações por entregador.
        # 2. .annotate(media=...): Cria um campo virtual 'media' contendo a média arredondada das notas.
        courier_reviews = CourierReview.objects.values('entregador__username').annotate(
            media=Round(Avg('value'))
        )
        
        # Transforma o resultado da consulta acima num dicionário Python simples para acesso rápido.
        # Exemplo: {'joao_delivery': 4, 'maria_moto': 5}
        avaliacoes_dict = {a['entregador__username']: a['media'] for a in courier_reviews}
        
        # Percorre a lista de entregadores e "cola" a média correspondente em cada objeto.
        # Isso permite usar {{ entregador.media }} diretamente no HTML, 
        # mesmo que esse campo não exista na tabela do usuário.
        for de in delivery_men:
            de.media = avaliacoes_dict.get(de.username)
        
        # Envia a lista processada para o template.
        return render(request, "manager/manager_delivery_man.html", {
            "delivery_men": delivery_men
        })

    except Exception as e:
        # Em caso de erro (ex: banco fora do ar, erro de importação),
        # registra no log e avisa o usuário sem quebrar a página inteira.
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
    """
    Carrega os dados de um entregador existente para edição e processa a atualização,
    mantendo a senha antiga caso uma nova não seja fornecida e validando os dados.
    """
    
    # Busca o entregador pelo ID. Se não existir, retorna erro 404.
    # Garante também que o usuário buscado é realmente do tipo 'DELIVERY_MAN'.
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')
    
    # Armazena a senha atual (já criptografada) numa variável auxiliar.
    # Isso é crucial: se o gerente deixar o campo de senha vazio no formulário,
    # não queremos salvar uma senha vazia, queremos manter a antiga.
    initial_password = delivery_man.password 

    if request.method == "POST":
        # Carrega o formulário com os dados enviados (POST/FILES).
        # O parâmetro 'instance=delivery_man' avisa ao formulário que estamos a EDITAR este objeto específico.
        form = DeliveryRegisterForm(request.POST, request.FILES, instance=delivery_man)
        
        if form.is_valid():
            # Prepara o objeto, mas não salva no banco ainda (commit=False)
            delivery_man = form.save(commit=False)
            delivery_man.tipo_usuario = 'DELIVERY_MAN'

            # --- Validações Manuais (Idade) ---
            birth_date = form.cleaned_data.get('data_nascimento')
            if birth_date:
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    form.add_error('data_nascimento', 'O entregador deve ter pelo menos 18 anos de idade.')

            # --- Validações Manuais (CPF) ---
            cpf = re.sub(r'\D', '', form.cleaned_data.get('cpf', ''))
            if len(cpf) != 11:
                form.add_error('cpf', 'CPF inválido. Deve conter 11 números.')
            delivery_man.cpf = cpf

            # --- Validações Manuais (Telefone) ---
            telefone_numbers = re.sub(r'\D', '', form.cleaned_data.get('telefone', ''))
            if not telefone_numbers:
                form.add_error('telefone', 'Telefone obrigatório.')
            elif len(telefone_numbers) < 10 or len(telefone_numbers) > 11:
                form.add_error('telefone', 'Telefone inválido. Deve conter 10 ou 11 números.')
            else:
                delivery_man.telefone = telefone_numbers

            # --- Validações Manuais (Placa) ---
            placa = form.cleaned_data.get('placa_moto', '').upper().replace('-', '')
            if placa and not re.match(r'^[A-Z]{3}[0-9]{4}$', placa):
                form.add_error('placa_moto', 'Placa inválida. Deve estar no formato ABC-1234.')
            delivery_man.placa_moto = f"{placa[:3]}-{placa[3:]}" if placa else ''

            # --- Lógica da Senha ---
            raw_password = form.cleaned_data.get('password')
            if raw_password:
                # Se o usuário digitou algo no campo senha, criptografa e define a nova senha.
                delivery_man.set_password(raw_password)
            else:
                # Se o campo senha ficou vazio, recupera a senha antiga que guardamos no início.
                delivery_man.password = initial_password

            # Se houver erros manuais adicionados acima, re-renderiza a página com os avisos.
            if form.errors:
                return render(request, "manager/manager_delivery_man_edit.html", {
                    "form": form,
                    "delivery_man": delivery_man
                })

            # Salva as alterações finais no banco de dados.
            delivery_man.save()
            form.save_m2m() # Salva relações ManyToMany, se houverem.
            
            messages.success(request, "Entregador atualizado com sucesso!")
            return redirect('manager_delivery_man')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        # Método GET: Carrega o formulário preenchido com os dados atuais do banco (instance=delivery_man)
        form = DeliveryRegisterForm(instance=delivery_man)

    # Renderiza a página de edição
    return render(request, "manager/manager_delivery_man_edit.html", {
        "form": form,
        "delivery_man": delivery_man
    })

@manager_required('japapou.delete_customuser')
@csrf_protect
def manager_delivery_man_delete_view(request, id):
    """
    Localiza e exclui um entregador do banco de dados com base no ID fornecido.
    A exclusão ocorre apenas via requisição POST para garantir segurança, 
    registrando a ação em logs e notificando o administrador.
    """
    
    # Busca o entregador pelo ID. 
    # O filtro 'tipo_usuario' garante que não excluímos acidentalmente um Administrador ou Cliente.
    # Se não encontrar, retorna erro 404.
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    # Verificação de segurança CRUCIAL:
    # Ações destrutivas (como deletar) nunca devem ser feitas via GET (apenas visitando a URL).
    # Exigir POST garante que a ação veio de um formulário ou botão de confirmação.
    if request.method == "POST":
        try:
            # Guarda o nome numa variável antes de deletar o objeto, 
            # para podermos usar o nome na mensagem de sucesso depois.
            delivery_man_name = delivery_man.username
            
            # Executa a exclusão definitiva do registo no banco de dados.
            delivery_man.delete() 
            
            # Regista a ação nos logs do sistema (útil para auditoria: saber "quem" deletou "quem").
            logger.info(f"Delivery man {delivery_man_name} deleted by {request.user.username}")
            
            # Envia mensagem visual de sucesso para o utilizador.
            messages.success(request, f"Entregador {delivery_man_name} excluído com sucesso!")
            
        except Exception as e:
            # Se houver algum erro no banco de dados (ex: integridade referencial),
            # captura o erro, registo no log e avisa o utilizador.
            logger.error(f"Error deleting delivery man {id}: {str(e)}")
            messages.error(request, f"Erro ao excluir entregador: {e}")

    # Independente se deletou ou se não foi POST, redireciona de volta para a lista de entregadores.
    return redirect('manager_delivery_man')