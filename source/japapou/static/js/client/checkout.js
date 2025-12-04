const modalEnderecos = document.getElementById("modal-enderecos");
const listaEnderecos = document.querySelectorAll(".endereco-item");
const tituloEnderecoSelecionado = document.getElementById("titulo-endereco-selecionado");
const complementoEnderecoSelecionado = document.getElementById("complemento-endereco-selecionado");
const inputEnderecoId = document.getElementById("input-endereco-id");

// fechar o modal ao clicar fora dele
modalEnderecos.addEventListener('click', (event) => {
  // Verifica se o clique ocorreu fora do conteúdo principal do dialog (não no ::backdrop)
  if (event.target === modalEnderecos) {
    modalEnderecos.close();
  }
});

listaEnderecos.forEach(item => {
    item.addEventListener('click', function() {
        // 1. Remove a classe 'selecionado' de todos os itens
        listaEnderecos.forEach(i => i.classList.remove('selecionado'));

        // 2. Adiciona a classe 'selecionado' no item clicado
        this.classList.add('selecionado');
        
        // 3. Captura os dados
        const id = this.getAttribute('data-id');
        const logradouro = this.getAttribute('data-logradouro');
        const numero = this.getAttribute('data-numero');
        const bairro = this.getAttribute('data-bairro');
        const complemento = this.getAttribute('data-complemento');
        
        // 4. Atualiza o input escondido para enviar o ID no formulário
        inputEnderecoId.value = id;

        // 5. Atualiza o texto na página principal (fora do modal)
        tituloEnderecoSelecionado.innerHTML = `${bairro}, ${logradouro}, ${numero}`;
        
        console.log(complemento);

        if (complemento !== "Sem Complemento") {
            complementoEnderecoSelecionado.innerHTML = `${complemento}`;
        }
        else {
            complementoEnderecoSelecionado.innerHTML = "Sem Complemento.";
        }
        
        
        // 7. Acessório: Garante que o tipo de pedido 'Entrega' esteja marcado
        //    (Pode ser útil para a lógica da função 'verificarTipoPedido')
        document.getElementById('entrega').checked = true;
        verificarTipoPedido();

        if (document.getElementById('pagamento-pix').checked) {
            atualizarPixViaAjax();
        }
    });
});


const inputRetirada = document.getElementById("retirada"); // elemento html do input retirada
const inputEntrega = document.getElementById("entrega"); // elemento html do input entrega


const blocoEndereco = document.getElementById("bloco-enderecos");
const labelRetirada = document.getElementById("label-retirada");
const labelEntrega = document.getElementById("label-entrega");
const divTipoDeEntrega = document.getElementById("tipo-entrega");
// const opcaoEntregaExpress = document.getElementById("express-opcao");

const modalMetodoPagamento = document.getElementById("modal-tipo-pagamento");
const inputCategoriaOnline = document.getElementById("categoria-online");
const inputCategoriaLocal = document.getElementById("categoria-local");
const labelCategoriaOnline = document.getElementById("label-categoria-online");
const labelCategoriaLocal = document.getElementById("label-categoria-local");
const divMetodoPagamento = document.getElementById("container-metodo-pagamento");
const containerMetodoOnline = document.getElementById("container-metodo-online");
const containerMetodoLocal = document.getElementById("container-metodo-local");
const divMetodoAtual = document.getElementById("mostrar-metodo-atual-online");
const divMetodoAtualLocal = document.getElementById("mostrar-metodo-atual-local");
const divRadioGroupCategoria = document.getElementById("radio-group-categoria");
const divContainerPix = document.getElementById("container-pix");
const divContainerCartao = document.getElementById("container-cartao");
const divContainerDinheiro = document.getElementById("container-dinheiro");
const inputMetodoDinheiro = document.getElementById("pagamento-dinheiro");
const inputMetodoPix = document.getElementById("pagamento-pix");
const inputMetodoCartao = document.getElementById("pagamento-cartao");

// função para verificar qual dos dois inputs está selecionado
function verificarTipoPedido() {

   // --- CASO 1: RETIRADA ---
    if (inputRetirada.checked) {
        console.log("Modo Retirada Ativado");

        // 1. Desativar a escolha de endereço (Visualmente e funcionalmente)
        blocoEndereco.style.opacity = "60%"; 
        blocoEndereco.style.pointerEvents = "none"; 
        
        containerMetodoOnline.style.display = "block";
        divMetodoAtual.style.display = "flex";
        divContainerPix.style.display = "block";
        

        // Estilização das etiquetas (labels)
        labelEntrega.style.opacity = "60%";
        labelRetirada.style.opacity = "100%";
        labelCategoriaLocal.style.pointerEvents = "none";
        labelCategoriaLocal.style.opacity = "30%";
        labelCategoriaOnline.style.opacity = "100%";
        
        // Desativar a visualização da taxa de entrega
        divTipoDeEntrega.style.opacity = "60%";

        // 2. GARANTIR QUE O PAGAMENTO ESTÁ ATIVO (Aqui estava o erro)
        // Precisamos garantir que pointerEvents seja 'all' e opacidade 100%
        divRadioGroupCategoria.style.pointerEvents = "all";
        divMetodoAtual.style.pointerEvents = "all";
        divMetodoPagamento.style.opacity = "100%";
     
        if(inputCategoriaLocal.checked === true) {
            console.log("mudando input categoria local para false...")
            inputCategoriaLocal.checked = false;
            inputCategoriaOnline.checked = true;
            divMetodoAtualLocal.style.display = "none";
        }

        console.log(inputCategoriaLocal.checked);
        console.log(inputCategoriaOnline.checked);

        // Chama a função para zerar a taxa (Backend/Visual)
        atualizarValoresResumo(false);
    }

    // --- CASO 2: ENTREGA ---
    if (inputEntrega.checked) {
        console.log("Modo Entrega Ativado");

        // 1. Ativar a escolha de endereço
        blocoEndereco.style.opacity = "100%";
        blocoEndereco.style.pointerEvents = "all";

        // Estilização das etiquetas
        labelRetirada.style.opacity = "60%";
        labelEntrega.style.opacity = "100%";
        labelCategoriaLocal.style.opacity = "60%";
        labelCategoriaLocal.style.pointerEvents = "all";
        
        
        // Ativar visualização da taxa
        divTipoDeEntrega.style.opacity = "100%";

        // 2. Garantir que o pagamento está ativo
        divRadioGroupCategoria.style.pointerEvents = "all";
        divMetodoAtual.style.pointerEvents = "all";
        divMetodoPagamento.style.opacity = "100%";
   

        console.log(inputCategoriaLocal.checked);
        console.log(inputCategoriaOnline.checked);

        // Chama a função para cobrar a taxa
        atualizarValoresResumo(true);
    }


    if (document.getElementById('pagamento-pix').checked) {
        atualizarPixViaAjax();
    }
}

function atualizarValoresResumo(comEntrega) {
    const elSubtotal = document.getElementById('resumo-subtotal');
    const elTaxa = document.getElementById('resumo-taxa');
    const elTotal = document.getElementById('resumo-total');

    if (!elSubtotal || !elTaxa || !elTotal) return;

    // 1. Pega os valores numéricos limpos dos atributos data-valor
    const subtotal = parseFloat(elSubtotal.getAttribute('data-valor'));
    const taxaOriginal = parseFloat(elTaxa.getAttribute('data-valor'));

    let novoTotal = 0;

    if (comEntrega) {
        // Soma a taxa
        novoTotal = subtotal + taxaOriginal;
        
        // Restaura o texto da taxa
        elTaxa.textContent = `R$ ${taxaOriginal.toFixed(2).replace('.', ',')}`;
        elTaxa.style.textDecoration = "none"; // Remove risco se houver
        elTaxa.style.color = "inherit";
    } else {
        // Sem taxa (Retirada)
        novoTotal = subtotal;

        // Mostra que é Grátis ou Riscado
        elTaxa.innerHTML = '<span style="text-decoration: line-through;">R$ ' + taxaOriginal.toFixed(2).replace('.', ',');
    }

    // 2. Atualiza o Total na tela (formatando para PT-BR: troca ponto por vírgula)
    elTotal.textContent = `R$ ${novoTotal.toFixed(2).replace('.', ',')}`;
}


function verificarTipoPagamento() {
    // se o input categoria online tiver selecionado 
    if (inputCategoriaOnline.checked) {
        labelCategoriaLocal.style.opacity = "60%";
        labelCategoriaOnline.style.opacity = "100%";
        divMetodoAtual.style.display = "flex";
        divMetodoAtualLocal.style.display = "none";


        inputMetodoPix.disabled = false;
        inputMetodoCartao.disabled = false;
        inputMetodoDinheiro.disabled = true;

        divContainerDinheiro.style.display = "none";

        if(inputMetodoPix.checked) {
            divContainerPix.style.display = "block";
            divContainerCartao.style.display = "none";
        }

        if(inputMetodoCartao.checked) {
            divContainerPix.style.display = "none";
            divContainerCartao.style.display = "block";
        }

    }

    // se o input categoria local tiver selecionado
    if (inputCategoriaLocal.checked) {
        labelCategoriaLocal.style.opacity = "100%";
        labelCategoriaOnline.style.opacity = "60%";
        divMetodoAtual.style.display = "none";
        divMetodoAtualLocal.style.display = "block";

        divContainerPix.style.display = "none";
        divContainerCartao.style.display = "none";

        inputMetodoPix.disabled = true;
        inputMetodoCartao.disabled = true;
        
        // Ativamos o método dinheiro
        inputMetodoDinheiro.disabled = false;

        if(inputMetodoDinheiro.checked) {
            divContainerDinheiro.style.display = "block";
        }
        else {
            divContainerDinheiro.style.display = "none";
        }
        
    }

    modalMetodoPagamento.close();
}



inputEntrega.addEventListener('change', verificarTipoPedido);
inputRetirada.addEventListener('change', verificarTipoPedido);
inputCategoriaLocal.addEventListener('change', verificarTipoPagamento);
inputCategoriaOnline.addEventListener('change', verificarTipoPagamento);

inputMetodoPix.addEventListener('change', verificarTipoPagamento);
inputMetodoCartao.addEventListener('change', verificarTipoPagamento);
inputMetodoDinheiro.addEventListener('change', verificarTipoPagamento);

document.addEventListener('DOMContentLoaded', () => {
    
    const btnCopiar = document.getElementById('btn-copiar-pix-final');
        if (btnCopiar) {
            btnCopiar.addEventListener('click', copiarPix);
    }

// Coverflow
  const slides = document.querySelectorAll('.slide');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  let current = slides.length >= 3 ? 1 : 0; // Inicia no segundo slide (índice 1) se houver 3 ou mais.

  function updateSlides() {
    slides.forEach((slide, i) => {
      const offset = i - current;
      const absOffset = Math.abs(offset);
      const prato = slide.querySelector('.prato');
      const especificacao = slide.querySelector('.especificacao');
      const circ_2 = slide.querySelector('.circ-2>p');
      const circ_1 = slide.querySelector('.circ-1');
      const maxVisible = 2; // Garante que os slides -2, -1, 0, 1, 2 são processados

      if (absOffset > maxVisible) {
        slide.style.opacity = '0';
        slide.style.pointerEvents = 'none';
        
        // Mantém a centralização mesmo quando o slide está fora de vista
        slide.style.transform = 'scale(0.5) translate(-50%, -50%)'; 
        slide.style.zIndex = 0;
        return;
      }

      slide.style.opacity = '1';
      slide.style.pointerEvents = 'auto';
      slide.style.zIndex = 10 - absOffset;

      // Movimento ajustado (0.65 da largura do slide para não sair da tela)
      const slideMovement = slides[0].offsetWidth * 0.9;
      
      // CRUCIAL: Esta transformação compensa o position: absolute (top: 50%; left: 50%) do CSS,
      // garantindo que o ponto de origem do slide é o centro do contêiner.
      const centeringTransform = 'translate(-50%, -50%)'; 

      if (offset === 0) {
        // Slide Central: Centrado + Sem translação X + Scale 1
        slide.style.transform = `${centeringTransform} translateX(0) scale(1)`;
        if (prato) prato.style.color = 'white';
        if (especificacao) especificacao.style.backgroundColor = 'var(--azul-mais-escuro)';
        if (circ_2) circ_2.style.color = 'var(--azul-mais-escuro)';
        if (circ_1) circ_1.style.backgroundColor = 'var(--azul-mais-escuro)';
        slide.style.pointerEvents = "all";
      } 
      else {
        // Slides Laterais: Centrado + Translação X (offset * slideMovement) + Scale 0.7
        slide.style.transform = `${centeringTransform} translateX(${offset * slideMovement}px) scale(0.7)`;
        if (prato) prato.style.color = 'white';
        if (especificacao) especificacao.style.backgroundColor = 'var(--vermelho)';
        if (circ_2) circ_2.style.color = 'var(--vermelho)';
        if (circ_1) circ_1.style.backgroundColor = 'var(--vermelho)';
        slide.style.pointerEvents = "none";
      }
    });
  }

  function goNext() { 
        if (current < slides.length - 1) { 
            current++; 
            updateSlides(); 
        } 
    }

    function goPrev() { 
        if (current > 0) { 
            current--; 
            updateSlides(); 
        } 
    }
    
    prevBtn.addEventListener('click', goPrev);
    nextBtn.addEventListener('click', goNext);

    // Se houver menos de 3 slides, desativa os botões 
    if (slides.length < 3) {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    }

    updateSlides();
    
    // 1. Executa a função para aplicar os estilos iniciais (opacidade/pointer-events)
    //    com base no input de rádio pre-selecionado no HTML.
    verificarTipoPedido();
    verificarTipoPagamento();

    // 2. Marca o endereço padrão no modal (se houver um ID pre-definido)
    const enderecoIdInicial = inputEnderecoId.value;
    if (enderecoIdInicial) {
        // Encontra o item do modal correspondente e adiciona a classe 'selecionado'
        const itemPadrao = document.querySelector(`.endereco-item[data-id="${enderecoIdInicial}"]`);
        if (itemPadrao) {
            itemPadrao.classList.add('selecionado');
        }
    }

});

function copiarPix() {
    // 1. Encontra o elemento 'textarea' que contém o código Pix.
    // Assumimos que a textarea tem um ID, por exemplo, 'codigo-pix-area'
    // **NOTA:** Ajusta o ID abaixo ('codigo-pix-area') para o ID real da tua textarea!
    const pixCodeElement = document.getElementById('codigo-pix-area');

    if (!pixCodeElement) {
        console.error("Elemento da área de texto do Pix não encontrado.");
        return; // Sai da função se a área de texto não existir
    }

    try {
        // 2. Tenta usar a API moderna (navigator.clipboard)
        // Esta é a forma mais recomendada e assíncrona
        navigator.clipboard.writeText(pixCodeElement.value)
            .then(() => {
                console.log("Código Pix copiado com sucesso (API moderna)!");
                
                // Feedback visual (Opcional)
                const btn = document.getElementById('btn-copiar-pix-final');
                if (btn) {
                    const originalText = btn.innerHTML;
                    btn.innerHTML = 'Copiado!';
                    
                    // Volta ao texto original após 2 segundos
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                    }, 2000);
                }
            })
            .catch(err => {
                // Se a API moderna falhar (geralmente por permissões), usa o método de fallback
                console.warn('Falha ao usar a API moderna. Usando método de fallback...', err);
                fallbackCopyTextToClipboard(pixCodeElement);
            });

    } catch (err) {
        // 3. Fallback para métodos mais antigos (sincronizados)
        console.warn('Navegador não suporta navigator.clipboard. Usando método de fallback.');
        fallbackCopyTextToClipboard(pixCodeElement);
    }
}

// Função de fallback para navegadores mais antigos (usa document.execCommand)
function fallbackCopyTextToClipboard(element) {
    // Seleciona o texto na textarea
    element.select();
    element.setSelectionRange(0, 99999); // Para dispositivos móveis

    try {
        // Executa o comando de cópia
        document.execCommand('copy');
        console.log('Código Pix copiado com sucesso (Fallback)!');

        // Feedback visual
        const btn = document.getElementById('btn-copiar-pix-final');
        if (btn) {
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Copiado!';
            
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 2000);
        }
    } catch (err) {
        console.error('Falha ao tentar copiar o texto por comando: ', err);
        alert('Falha ao copiar o código Pix. Por favor, selecione e copie manualmente.');
    }
}

async function atualizarPixViaAjax() {
    const form = document.getElementById('form-checkout');
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    // Cria um objeto com os dados do formulário atual
    const formData = new FormData(form);
    
    // Força o método de pagamento ser PIX para gerar o código
    formData.set('metodo_pagamento', 'PIX'); 

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Importante para o Django saber que é AJAX
                'X-CSRFToken': csrfToken
            },
            body: formData
        });

        const data = await response.json();

        if (data.sucesso) {
            console.log("Pix atualizado!", data);

            // 1. Atualizar a imagem do QR Code
            const imgQr = document.getElementById('img-qr-code');
            if (imgQr) {
                imgQr.src = `data:image/png;base64,${data.qr_code_base64}`;
            }

            // 2. Atualizar o Textarea (Copia e Cola)
            const txtPix = document.getElementById('codigo-pix-copia');
            if (txtPix) {
                txtPix.value = data.codigo_pix;
            }

            // 3. (Opcional) Garantir que o valor total na tela bata com o do Pix
            // Embora a tua função 'atualizarValoresResumo' já faça isso visualmente,
            // aqui garantimos que o valor veio do backend.
            const elTotal = document.getElementById('resumo-total');
            if(elTotal) elTotal.innerText = `R$ ${data.total_formatado}`;

        } else {
            console.error("Erro ao gerar Pix:", data.erro);
        }

    } catch (error) {
        console.error("Erro na requisição AJAX:", error);
    }
}



// 1. Inicializa o Stripe com a tua CHAVE PÚBLICA
const stripe = Stripe(STRIPE_PUBLIC_KEY);
const elements = stripe.elements();

// 2. Cria e monta o elemento do cartão
const card = elements.create('card', {
    style: {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    }
});
// Só monta se o elemento existir na página
if (document.getElementById('card-element')) {
    card.mount('#card-element');
}

// 3. Intercepta o envio do formulário
const formCheckout = document.getElementById('form-checkout');

formCheckout.addEventListener('submit', async (event) => {
    // Verifica se o método selecionado é Cartão
    const isCartao = document.getElementById('categoria-online').checked && 
                     document.getElementById('pagamento-cartao').checked;

    if (isCartao) {
        event.preventDefault(); // Impede o envio imediato

        console.log("Processando Stripe...");

        // Cria o Método de Pagamento no Stripe
        const result = await stripe.createPaymentMethod({
            type: 'card',
            card: card,
            billing_details: {
                // Podes adicionar dados do utilizador aqui se quiseres
                // name: 'Nome do Cliente',
            },
        });

        if (result.error) {
            // Mostra erro ao utilizador
            const errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Sucesso! Temos o ID (ex: pm_12345...)
            console.log("PaymentMethod ID:", result.paymentMethod.id);
            
            // Coloca o ID no input hidden e envia o formulário
            document.getElementById('stripePaymentMethodId').value = result.paymentMethod.id;
            formCheckout.submit();
        }
    }
});