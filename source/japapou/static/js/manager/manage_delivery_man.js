document.addEventListener("DOMContentLoaded", () => {
    const addCard = document.getElementById("add-card");

    if (addCard) {
        addCard.addEventListener("mousedown", () => {
            addCard.style.transform = "scale(0.97)";
        });
        addCard.addEventListener("mouseup", () => {
            addCard.style.transform = "scale(1)";
        });
    }

    console.log("Script de gerenciamento de entregadores carregado.");
    const cards = document.querySelectorAll(".card");
    
    // Verificação de segurança
    if (cards.length === 0) {
        console.warn("Nenhum elemento com a classe .card foi encontrado.");
        return;
    }

    cards.forEach(card => {
        // Pega o valor e garante que a vírgula vira ponto
        let rawMedia = card.dataset.media;
        
        if (!rawMedia) {
             console.error("Falta o atributo data-media neste card:", card);
             return; 
        }

        // Substitui virgula por ponto para garantir compatibilidade PT-BR
        let media = parseFloat(rawMedia.replace(',', '.'));
        
        console.log(`Card encontrado. Média original: ${rawMedia} | Média processada: ${media}`);

        const estrelas = card.querySelectorAll(".star");

        estrelas.forEach((star, index) => {
            // Lógica: Se a média for 3, o índice 0, 1, 2 são menores (amarelos).
            // O índice 3 é igual (vira cinza). O índice 4 é maior (vira cinza).
            if (index >= media) {
                star.classList.add("star-inactive");
            } else {
                // Remove caso haja alguma lógica de re-renderização
                star.classList.remove("star-inactive"); 
            }
        });
    });

});
