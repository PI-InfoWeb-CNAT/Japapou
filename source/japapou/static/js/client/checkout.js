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
    });
});


const inputRetirada = document.getElementById("retirada"); // elemento html do input retirada
const inputEntrega = document.getElementById("entrega"); // elemento html do input entrega


const blocoEndereco = document.getElementById("bloco-enderecos");
const labelRetirada = document.getElementById("label-retirada");
const labelEntrega = document.getElementById("label-entrega");
const divTipoDeEntrega = document.getElementById("tipo-entrega");
// const opcaoEntregaExpress = document.getElementById("express-opcao");

const inputCategoriaOnline = document.getElementById("categoria-online");
const inputCategoriaLocal = document.getElementById("categoria-local");
const labelCategoriaOnline = document.getElementById("label-categoria-online");
const labelCategoriaLocal = document.getElementById("label-categoria-local");
const divMetodoPagamento = document.getElementById("container-metodo-pagamento");
const divMetodoAtual = document.getElementById("mostrar-metodo-atual-online");
const divMetodoAtualLocal = document.getElementById("mostrar-metodo-atual-local");
const divRadioGroupCategoria = document.getElementById("radio-group-categoria");


// função para verificar qual dos dois inputs está selecionado
function verificarTipoPedido() {

    // se o input retirada estiver selecionado...
    if (inputRetirada.checked) {
        console.log("input retirada: ", inputRetirada);

        blocoEndereco.style.opacity = "60%"; // diminui a opacidade 
        labelEntrega.style.opacity = "60%";
        labelRetirada.style.opacity = "100%";
        blocoEndereco.style.pointerEvents = "none"; // faz com que toda a area da div não de para ser alterada por eventos de click
        
        divRadioGroupCategoria.style.pointerEvents = "none";
        divMetodoAtual.style.pointerEvents = "none";
        divMetodoPagamento.style.opacity = "60%";
        blocoEndereco.style.pointerEvents = "none";
        // opcaoEntregaExpress.style.opacity = "60%";
        divTipoDeEntrega.style.opacity = "60%";
        // divTipoDeEntrega.style.pointerEvents = "none";
    }

    if (inputEntrega.checked) {
        console.log("input entrega: ", inputEntrega);

        blocoEndereco.style.opacity = "100%";
        labelRetirada.style.opacity = "60%";
        labelEntrega.style.opacity = "100%";
        blocoEndereco.style.pointerEvents = "all";

        divRadioGroupCategoria.style.pointerEvents = "all";
        divMetodoAtual.style.pointerEvents = "all";
        divMetodoPagamento.style.opacity = "100%";
        blocoEndereco.style.pointerEvents = "all";
        // opcaoEntregaExpress.style.opacity = "60%";
        divTipoDeEntrega.style.opacity = "100%";
        // divTipoDeEntrega.style.pointerEvents = "none";
    }
}

function verificarTipoPagamento() {
    // se o input categoria online tiver selecionado 
    if (inputCategoriaOnline.checked) {
        labelCategoriaLocal.style.opacity = "60%";
        labelCategoriaOnline.style.opacity = "100%";
        divMetodoAtual.style.display = "flex";
        divMetodoAtualLocal.style.display = "none";
    }

    // se o input categoria local tiver selecionado
    if (inputCategoriaLocal.checked) {
        labelCategoriaLocal.style.opacity = "100%";
        labelCategoriaOnline.style.opacity = "60%";
        divMetodoAtual.style.display = "none";
        divMetodoAtualLocal.style.display = "block";
        
    }
}

inputEntrega.addEventListener('change', verificarTipoPedido);
inputRetirada.addEventListener('change', verificarTipoPedido);
inputCategoriaLocal.addEventListener('change', verificarTipoPagamento);
inputCategoriaOnline.addEventListener('change', verificarTipoPagamento);

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
});
