const elementoSelect = document.querySelector(".frete-dropdown");

const opcoes = elementoSelect.options;

var totalValorHtml = document.querySelector(".total-valor"); // contem a tag html
var totalValorString = document.querySelector(".total-valor").textContent; // contem o valor da tag html

const elementoDados = document.getElementById('dados-do-django'); 

var floatTotalValor = parseFloat(totalValorString.replace("R$", '').replace(',','.').replace(' ',''));

// console.log(totalValorString)
if (elementoDados) {
    // 2. Extrai o conteúdo (que é a string JSON)
    const stringJson = elementoDados.textContent;
    // console.log("String json", stringJson)
    // 3. Converte a string JSON num objeto JavaScript
    try {
        const dadosDoDjango = JSON.parse(stringJson);

        // 4. Agora você pode usar os dados!
        taxaEntrega = dadosDoDjango.taxa_entrega;


    } catch (e) {
        console.error("Erro ao analisar o JSON:", e);
    }
}

function somarValorTotal() {
    // se a opção selecionada for a opção de entrega
    if(elementoSelect.selectedIndex === 2) {
        // console.log("Opção 3 escolhida");

        floatTotalValor += taxaEntrega // adicionando a taxa de entrega ao valor do pedido
        // console.log(floattotalValorStringString);

        var novoValor = "R$" + ' ' + floatTotalValor.toFixed(2);
        novoValor = novoValor.replace('.',',');
        // console.log(novoValor)

        totalValorHtml.textContent = novoValor; // atualiza o valor no html
    }
    else {
        totalValorHtml.textContent = totalValorString;
    }

    taxaEntrega = 0; // zerar taxa de entrega para que o valor nao fique subindo infinitamente
    
    // console.log(`Índice selecionado: ${indiceSelecionado}`);
    // console.log(`Valor da opção no índice: ${opcaoSelecionada.textContent}`);
}

elementoSelect.addEventListener('change', somarValorTotal);