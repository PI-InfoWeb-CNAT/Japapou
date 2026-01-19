from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from japapou.forms import EnderecoForm
from japapou.models import Endereco


    
@login_required
def add_endereco_view(request):
    """
    Controla a página para adicionar um novo endereço.
    GET: Mostra o formulário vazio.
    POST: Valida os dados, salva o novo endereço e redireciona 
          de volta para o checkout.
    """
    
    # --- Lógica do POST (Salvando o formulário) ---
    if request.method == 'POST':
        # Cria uma instância do formulário com os dados enviados (request.POST)
        form = EnderecoForm(request.POST)
        
        if form.is_valid():
            # O formulário é válido.
            # Não salve ainda (commit=False), pois precisamos 
            # adicionar o usuário dono deste endereço.
            novo_endereco = form.save(commit=False)
            
            # Adiciona o usuário logado como o "dono" do endereço
            novo_endereco.usuario = request.user
            
            # Agora sim, salva no banco de dados
            novo_endereco.save()

            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)
            
            # Redireciona de volta ao checkout!
            return redirect('client_profile')
        
        else:
            # Se o formulário for inválido (ex: campo 'cep' vazio),
            # o Django automaticamente preparará as mensagens de erro.
            # Apenas renderizamos a página novamente com o 'form' preenchido.
            messages.error(request, "Por favor, corrija os erros no formulário.")
            # O código abaixo cuidará de re-renderizar
            next_url = request.GET.get('next')

    # --- Lógica do GET (Mostrando o formulário) ---
    else:
        # Se for um GET, apenas crie um formulário vazio
        form = EnderecoForm()
        next_url = request.GET.get('next')

    # Contexto para o template
    contexto = {
        'form': form,
        'next_url': next_url,
    }
    
    # Renderiza o template com o formulário
    return render(request, 'client/add_endereco.html', contexto)

@login_required
def listar_enderecos_view(request):
    """
    Controla a página para listar os endereços do usuário logado.
    """
    # Obtém todos os endereços do usuário logado
    enderecos = Endereco.objects.filter(usuario=request.user)
    
    contexto = {
        'enderecos': enderecos
    }
    
    return render(request, 'client/enderecos.html', contexto)


@login_required
def editar_endereco_view(request, endereco_id):
    """
    Controla a edição de um endereço existente.
    Recebe 'endereco_id' para saber qual registo buscar no banco.
    """
    
    # 1. Busca o endereço pelo ID. Se não existir, dá erro 404 automaticamente.
    endereco = get_object_or_404(Endereco, id=endereco_id)
    
    # 2. Segurança: Verifica se o endereço pertence ao usuário logado.
    if endereco.usuario != request.user:
        messages.error(request, "Você não tem permissão para editar este endereço.")
        return redirect('client_profile')

    # --- Lógica do POST (Salvando a edição) ---
    if request.method == 'POST':
        # Aqui está o segredo: passamos 'instance=endereco'.
        # Isso diz ao form: "Atualize ESTE endereço, não crie um novo".
        form = EnderecoForm(request.POST, instance=endereco)
        
        if form.is_valid():
            form.save()
            
            # Lógica de redirecionamento inteligente (igual ao adicionar)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('client_profile')
        else:
            messages.error(request, "Corrija os erros no formulário.")
            next_url = request.POST.get('next')

    # --- Lógica do GET (Carregando o formulário preenchido) ---
    else:
        # No GET, também passamos 'instance=endereco' para o formulário
        # aparecer preenchido com os dados atuais.
        form = EnderecoForm(instance=endereco)
        next_url = request.GET.get('next')

    contexto = {
        'form': form,
        'next_url': next_url,
        'endereco': endereco # Passamos o objeto caso queiras usar no título (ex: "Editar Endereço #1")
    }
    
    # Podemos reutilizar o mesmo template de adicionar ou criar um específico
    return render(request, 'client/add_endereco.html', contexto)