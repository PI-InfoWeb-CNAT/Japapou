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

    inputCategoriaLocal.addEventListener('change', console.log("input categoria local", inputCategoriaLocal.checked));
    inputCategoriaOnline.addEventListener('change', console.log("input categoria online", inputCategoriaOnline.checked));

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

    const btnCopiar = document.getElementById('btn-copiar-pix-final');
        if (btnCopiar) {
            btnCopiar.addEventListener('click', copiarPix);
    }

});

function copiarPix() {
    const codigoInput = document.getElementById('codigo-pix-copia');
    if (codigoInput) {
        codigoInput.select();
        codigoInput.setSelectionRange(0, 99999); // Mobile
        
        // Tenta API moderna, fallback para antigo
        if (navigator.clipboard) {
            navigator.clipboard.writeText(codigoInput.value)
                .then(() => alert('Código PIX copiado!'))
                .catch(() => alert('Erro ao copiar.'));
        } else {
            document.execCommand('copy');
            alert('Código PIX copiado!');
        }
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