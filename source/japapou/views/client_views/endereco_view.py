from django.shortcuts import render, redirect # type: ignore
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
            
            messages.success(request, "Novo endereço salvo com sucesso!")
            
            # Redireciona de volta ao checkout!
            return redirect('client_profile')
        
        else:
            # Se o formulário for inválido (ex: campo 'cep' vazio),
            # o Django automaticamente preparará as mensagens de erro.
            # Apenas renderizamos a página novamente com o 'form' preenchido.
            messages.error(request, "Por favor, corrija os erros no formulário.")
            pass # O código abaixo cuidará de re-renderizar

    # --- Lógica do GET (Mostrando o formulário) ---
    else:
        # Se for um GET, apenas crie um formulário vazio
        form = EnderecoForm()

    # Contexto para o template
    contexto = {
        'form': form
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