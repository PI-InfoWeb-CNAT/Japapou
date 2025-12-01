from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.conf import settings
from django.contrib.auth.decorators import login_required # type: ignore
from django.db import transaction # type: ignore
from django.contrib import messages # type: ignore
from decimal import Decimal # Para lidar com a taxa de entrega
from japapou.models import Cart, Order, OrderItem, Endereco
from japapou.forms import EnderecoForm
from japapou.utils import gerar_pix_simulado
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

TAXA_ENTREGA = Decimal("5.00")

def _calcular_total_e_endereco(request, subtotal, enderecos_do_usuario):
    """
    Função auxiliar para calcular o total, taxa e obter o objeto Endereco 
    com base nos dados POST.
    Retorna (total_final, taxa, endereco_escolhido, tipo_pedido)
    """
    tipo_pedido = request.POST.get('tipo_pedido') 
    total_final = subtotal
    taxa = Decimal("0.00") 
    endereco_escolhido = None
    endereco_id_selecionado = request.POST.get('endereco_id')

    if tipo_pedido == Order.TipoPedido.ENTREGA:
        if not endereco_id_selecionado:
            return total_final, taxa, None, tipo_pedido, "Por favor, selecione um endereço para a entrega."
        
        try:
            endereco_escolhido = enderecos_do_usuario.get(id=endereco_id_selecionado)
        except Endereco.DoesNotExist:
            return total_final, taxa, None, tipo_pedido, "Endereço inválido selecionado."
        
        taxa = TAXA_ENTREGA
        total_final += taxa
        
    return total_final, taxa, endereco_escolhido, tipo_pedido, None


@login_required
@transaction.atomic
def checkout_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    METODOS_VALIDOS = [m[0] for m in Order.MetodoPagamento.choices]

    try:
        cart = request.user.cart 
        cart_items = cart.items.all() 
    except Cart.DoesNotExist:
        messages.error(request, "Seu carrinho não foi encontrado.")
        return redirect('home_page') 

    if not cart_items.exists():
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('cart_view') 

    subtotal = cart.get_cart_total()

    enderecos_do_usuario = request.user.enderecos.all()
    endereco_padrao = enderecos_do_usuario.first()
    tipo_pedido_padrao = Order.TipoPedido.ENTREGA if endereco_padrao else Order.TipoPedido.RETIRADA

    # Configuração de contexto inicial para o GET ou falha
    contexto_base = {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,

        'cart_items': cart_items,
        'subtotal': subtotal,
        'taxa_entrega': TAXA_ENTREGA, 
        'TipoPedido': Order.TipoPedido,
        'enderecos': enderecos_do_usuario,
        'endereco_padrao': endereco_padrao,
        'tipo_pedido_padrao': tipo_pedido_padrao,
        'MetodoPagamento': Order.MetodoPagamento,
        'metodo_selecionado_id': Order.MetodoPagamento.PIX, # PIX como padrão
        'categoria_selecionada': 'ONLINE',
    }
    # Atualizar o total no contexto_base para o GET
    taxa_inicial = TAXA_ENTREGA if tipo_pedido_padrao == Order.TipoPedido.ENTREGA else Decimal("0.00")
    contexto_base['total'] = subtotal + taxa_inicial


    if request.method == "POST":
        
        # Detetar se é uma chamada AJAX (JavaScript)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        metodo_pagamento = request.POST.get('metodo_pagamento')
        pix_confirmado = request.POST.get('pix_confirmado') 
        
        # Se for AJAX, assumimos que queremos recalcular para PIX ou validar totais
        if is_ajax and not metodo_pagamento:
            metodo_pagamento = Order.MetodoPagamento.PIX

        if not metodo_pagamento or metodo_pagamento not in METODOS_VALIDOS:
            if is_ajax:
                return JsonResponse({'sucesso': False, 'erro': 'Método inválido'})
            messages.error(request, "Por favor, escolha um método de pagamento válido.")
            return redirect('checkout')
        
        # 1. Calcular todos os detalhes do pedido
        total_final, taxa, endereco_escolhido, tipo_pedido, erro = _calcular_total_e_endereco(
            request, subtotal, enderecos_do_usuario
        )
        
        if erro:
            if is_ajax:
                 return JsonResponse({'sucesso': False, 'erro': erro})
            messages.error(request, erro)
            return redirect('checkout')
        
        # --- LÓGICA EXCLUSIVA PARA AJAX (Atualização do QR Code) ---
        if is_ajax:
            # Gera o novo Pix com o novo valor total
            codigo_pix, qr_code_base64 = gerar_pix_simulado(request.user.id, total_final)
            
            return JsonResponse({
                'sucesso': True,
                'qr_code_base64': qr_code_base64,
                'codigo_pix': codigo_pix,
                'total_formatado': f"{total_final:.2f}".replace('.', ','),
                'taxa_formatada': f"{taxa:.2f}".replace('.', ',')
            })
        
        # --- A. LÓGICA DO PIX (Primeira Submissão para Geração) ---
        if metodo_pagamento == Order.MetodoPagamento.PIX and not pix_confirmado:
            
            # Gera o código e o QR Code simulados (usa ID do user para unicidade)
            codigo_pix, qr_code_base64 = gerar_pix_simulado(request.user.id, total_final)
            

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'sucesso': True,
                    'qr_code_base64': qr_code_base64,
                    'codigo_pix': codigo_pix,
                    'total': str(total_final)
                })


            # Adiciona informações do Pix e o total recalculado ao contexto
            contexto_base.update({
                'total': total_final, 
                'pix_selecionado': True,
                'codigo_pix': codigo_pix,
                'qr_code_base64': qr_code_base64,
                'metodo_selecionado_id': metodo_pagamento, 
                'endereco_selecionado_id': request.POST.get('endereco_id'), # Mantém o estado do endereço
                'tipo_pedido_selecionado': tipo_pedido, # Mantém o estado do tipo de pedido
            })
            
            # Renderiza o checkout com a seção PIX visível
            return render(request, 'client/checkout.html', contexto_base)

        # --- B. LÓGICA DE CRIAÇÃO DO PEDIDO (Dinheiro, Cartão ou Pix Confirmado) ---
        
        troco_para = request.POST.get('troco_para')
        val_troco = None

        if metodo_pagamento == Order.MetodoPagamento.DINHEIRO and troco_para:
            try:
                # Converte para Decimal para salvar no banco
                val_troco = Decimal(troco_para.replace(',', '.'))

                if val_troco < total_final:
                    messages.error(request, f"O valor para troco (R$ {val_troco}) não pode ser menor que o total do pedido (R$ {total_final}).")
                    return redirect('checkout')
                
            except:
                val_troco = None

        # Determinar o status inicial
        if metodo_pagamento == Order.MetodoPagamento.PIX and pix_confirmado:
            # Se for Pix e o usuário clicou em 'Finalizar'
            status_inicial = Order.Status.PROCESSANDO # Já "pagou" (simulado), pode processar
        elif metodo_pagamento in [Order.MetodoPagamento.DINHEIRO, Order.MetodoPagamento.CARTAO]:
            # Pagamento na entrega, deve aguardar confirmação da loja/entrega
            status_inicial = Order.Status.PENDENTE 
        else:
             # Caso de segurança, deve ser tratado acima
             messages.error(request, "Erro desconhecido no método de pagamento.")
             return redirect('checkout')


        try:
            # 2. Criação do Objeto Order
            new_order = Order.objects.create(
                usuario=request.user,
                total=total_final,           
                estimate=total_final,        
                tipo_pedido=tipo_pedido,     
                taxa_entrega=taxa,
                endereco_entrega=endereco_escolhido, 
                metodo_pagamento=metodo_pagamento,
                status=status_inicial,
                troco_para=val_troco, # NOVO CAMPO
            )
            
            # 3. Criação dos OrderItem
            items_para_criar = []
            for item in cart_items:
                items_para_criar.append(
                    OrderItem(
                        preco_prato=item.plate.price, # preco do prato no momento da compra
                        order=new_order,
                        prato=item.plate,
                        amount=item.quantity,
                    )
                )
            OrderItem.objects.bulk_create(items_para_criar)

            # 4. Limpa o carrinho
            cart_items.delete()

            return redirect('order_success', order_id=new_order.id) 

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar seu pedido: {e}")
            return redirect('checkout') 

   
    else:
        # Lógica do GET

        if contexto_base['metodo_selecionado_id'] == Order.MetodoPagamento.PIX:
            
            # Usamos o total calculado no contexto_base (Subtotal + Taxa Inicial)
            total_inicial = contexto_base['total']
            
            codigo_pix, qr_code_base64 = gerar_pix_simulado(request.user.id, total_inicial)
            
            contexto_base.update({
                'pix_selecionado': True,  # Isso ativa o IF no HTML
                'codigo_pix': codigo_pix,
                'qr_code_base64': qr_code_base64,
            })

        return render(request, 'client/checkout.html', contexto_base)
    

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