from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db import transaction # type: ignore
from django.contrib import messages # type: ignore
from decimal import Decimal # Para lidar com a taxa de entrega
from japapou.models import Cart, Order, OrderItem, Endereco
from japapou.forms import EnderecoForm

TAXA_ENTREGA = Decimal("5.00")

@login_required
@transaction.atomic # Garante que todas as operações do banco de dados sejam atômicas, ou seja, todas ocorrem ou nenhuma ocorre.
def checkout_view(request):
    """
    Controla a página de checkout.
    GET: Mostra o resumo do carrinho e as opções de entrega/retirada.
    POST: Processa o pedido com base na escolha, "simula" o pagamento,
          cria o Order e limpa o carrinho.
    """
    
    
    try:
        cart = request.user.cart 
        cart_items = cart.items.all() 
    except Cart.DoesNotExist:
        # teoricamente não deveria acontecer, um cliente sempre deve ter um carrinho
        messages.error(request, "Seu carrinho não foi encontrado.")
        return redirect('home_page') 

    
    if not cart_items.exists():
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('cart_view') 

    
    subtotal = cart.get_cart_total()

    enderecos_do_usuario = request.user.enderecos.all()
    
    if request.method == "POST":
        
        
        tipo_pedido = request.POST.get('tipo_pedido') 

        if not tipo_pedido or tipo_pedido not in [Order.TipoPedido.ENTREGA, Order.TipoPedido.RETIRADA]:
            
            messages.error(request, "Por favor, escolha um método de entrega ou retirada.")
            return redirect('checkout') 

        
        total_final = subtotal
        taxa = Decimal("0.00")
        endereco_escolhido = None

        if tipo_pedido == Order.TipoPedido.ENTREGA:
            endereco_id_selecionado = request.POST.get('endereco_id')

            if not endereco_id_selecionado:
                messages.error(request, "Por favor, selecione um endereço para a entrega.")
                return redirect('checkout')
            
            try:
                
                endereco_escolhido = enderecos_do_usuario.get(id=endereco_id_selecionado)
            except Endereco.DoesNotExist:
                messages.error(request, "Endereço inválido selecionado.")
                return redirect('checkout')
            
            taxa = TAXA_ENTREGA
            total_final += taxa

        
        try:
            new_order = Order.objects.create(
                usuario=request.user,
                total=total_final,           
                estimate=total_final,        
                tipo_pedido=tipo_pedido,     
                taxa_entrega=taxa,
                endereco_entrega=endereco_escolhido,            
            )
            
            
            items_para_criar = []
            for item in cart_items:
                items_para_criar.append(
                    OrderItem(
                        order=new_order,
                        prato=item.plate,
                        amount=item.quantity,
                        
                    )
                )
            
            OrderItem.objects.bulk_create(items_para_criar) # bulkcreae para otimizar a inserção no banco de dados

            # limpa o carrinho
            cart_items.delete()

            
            #messages.success(request, f"Pedido #{new_order.id} criado com sucesso!")
            return redirect('order_success', order_id=new_order.id) 

        except Exception as e:
            # Em caso de erro, o @transaction.atomic reverte tudo.
            messages.error(request, f"Ocorreu um erro ao processar seu pedido: {e}")
            return redirect('checkout') 

   
    else:
        
        contexto = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'taxa_entrega': TAXA_ENTREGA, 
            'total_com_entrega': subtotal + TAXA_ENTREGA,
            'TipoPedido': Order.TipoPedido,
            'enderecos': enderecos_do_usuario,
        }
        
        
        return render(request, 'client/checkout.html', contexto)
    

@login_required
def order_success_view(request, order_id):
    pedido = get_object_or_404(Order, id=order_id, usuario=request.user)
    return render(request, 'client/order_success.html', {'pedido': pedido})

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
            
            # 💡 PONTO-CHAVE: Redireciona de volta ao checkout!
            return redirect('checkout')
        
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