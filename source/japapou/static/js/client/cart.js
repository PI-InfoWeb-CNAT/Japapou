// O código foi encapsulado em uma IIFE (Immediately Invoked Function Expression)
// para criar um escopo privado e evitar o erro "has already been declared".

(function() {
    // === Variáveis do DOM ===
    const elementoSelect = document.querySelector(".frete-dropdown");
    const totalValorHtml = document.querySelector(".total-valor"); // Contém a tag <div> que exibe o total

    // --- Lógica de Inicialização de Valores ---

    // Obtém a string de valor inicial do HTML (Ex: "R$ 100,00")
    const totalValorStringInicial = totalValorHtml.textContent.trim();

    // Função auxiliar para converter "R$ 100,00" para 100.00 (float)
    const stringToFloat = (str) => {
        // Remove "R$", espaços, substitui vírgula por ponto e converte para float
        return parseFloat(str.replace("R$", '').replace(/\s/g, '').replace(',', '.'));
    };

    // Variável para armazenar o valor base do carrinho (sem frete), crucial para resets
    let floatTotalValorBase = stringToFloat(totalValorStringInicial);

    // Variável para armazenar a taxa de entrega (padrão 0)
    let taxaEntrega = 0.00; 

    // Busca a taxa de entrega do Django (se existir)
    const elementoDados = document.getElementById('dados-do-django'); 

    if (elementoDados) {
        const stringJson = elementoDados.textContent;
        try {
            const dadosDoDjango = JSON.parse(stringJson);
            // Armazena a taxa de entrega para uso futuro
            taxaEntrega = parseFloat(dadosDoDjango.taxa_entrega); 

        } catch (e) {
            console.error("Erro ao analisar o JSON de dados do Django:", e);
        }
    }

    // --- Função de Cálculo e Atualização ---

    function atualizarValorTotal() {
        let novoTotal = floatTotalValorBase;
        
        const indiceSelecionado = elementoSelect.selectedIndex;

        // Se a opção de "Entrega Padrão" for selecionada (índice 2)
        if (indiceSelecionado === 2) {
            novoTotal += taxaEntrega;
        } 
        // Para as outras opções (0: Estimar Frete, 1: Retirada), o total permanece o valor base
        // (Assumindo que Retirada é R$ 0,00, o que já está implícito).

        // Formata o novo valor de volta para o formato de moeda "R$ 123,45"
        let novoValorFormatado = "R$ " + novoTotal.toFixed(2).replace('.', ',');
        
        // Atualiza o valor no HTML
        totalValorHtml.textContent = novoValorFormatado; 
    }

    // === Listener CRÍTICO ===
    // ATENÇÃO: Essa linha garante que a função de cálculo é chamada quando o usuário 
    // muda a opção no dropdown de frete. Este era um bug de funcionalidade no seu código.
    elementoSelect.addEventListener('change', atualizarValorTotal);

})(); // Fim da IIFE