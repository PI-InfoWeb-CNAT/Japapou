const inputRetirada = document.getElementById("retirada"); // elemento html do input retirada

const inputEntrega = document.getElementById("entrega"); // elemento html do input entrega

const blocoEndereco = document.getElementById("bloco-enderecos");


// função para verificar qual dos dois inputs está selecionado
function verificarTipoPedido() {

    // se o input retirada estiver selecionado...
    if (inputRetirada.checked) {
        console.log("input retirada: ", inputRetirada);

        blocoEndereco.style.opacity = "30%"; // diminui a opacidade 

        blocoEndereco.style.pointerEvents = "none"; // faz com que toda a area da div não de para ser alterada por eventos de click
    }

    if (inputEntrega.checked) {
        console.log("input entrega: ", inputEntrega);

        blocoEndereco.style.opacity = "100%";

        blocoEndereco.style.pointerEvents = "all";
    }
}

inputEntrega.addEventListener('change', verificarTipoPedido);
inputRetirada.addEventListener('change', verificarTipoPedido);
