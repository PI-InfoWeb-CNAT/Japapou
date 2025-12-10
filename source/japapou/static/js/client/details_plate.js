document.addEventListener('DOMContentLoaded', function() {
    const starWidget = document.getElementById('star-widget');
    if (starWidget) {
        const stars = starWidget.querySelectorAll('.star');
        
        // CORREÇÃO CRÍTICA: Mudamos para 'id_value' para corresponder ao ID padrão do Django
        // gerado por {{ form.value }}.
        const hiddenInput = document.getElementById('id_value'); 
        
        if (hiddenInput) {
            // Função para preencher/despreencher as estrelas
            function setStarRating(rating) {
                stars.forEach(star => {
                    const starValue = parseInt(star.dataset.value);
                    if (starValue <= rating) {
                        star.classList.add('filled');
                    } else {
                        star.classList.remove('filled');
                    }
                });
            }

            // Event listener para clique (para submeter a nota)
            starWidget.addEventListener('click', function(e) {
                // Adiciona .closest('.star') para garantir que a nota seja registrada 
                // mesmo se o usuário clicar no ÍCONE (i) dentro do SPAN (.star).
                const starElement = e.target.closest('.star'); 
                if (starElement) {
                    const rating = parseInt(starElement.dataset.value);
                    hiddenInput.value = rating; // ESCREVE a nova nota no campo oculto
                    setStarRating(rating);
                }
            });

            // Event listener para mouseover (efeito visual)
            starWidget.addEventListener('mouseover', function(e) {
                const starElement = e.target.closest('.star');
                if (starElement) {
                    const hoverRating = parseInt(starElement.dataset.value);
                    setStarRating(hoverRating);
                }
            });

            // Event listener para mouseout (restaura a nota atual)
            starWidget.addEventListener('mouseout', function() {
                const currentRating = parseInt(hiddenInput.value) || 0;
                setStarRating(currentRating);
            });

            // Inicializa as estrelas com o valor existente (para edição)
            const initialRating = parseInt(hiddenInput.value) || 0;
            setStarRating(initialRating);
            
        } else {
             // Mantenha este log para ajudar no debugging do HTML
             console.error("ERRO: Campo oculto de avaliação (id_value) não encontrado. Garanta que {{ form.value }} esteja no rating.html.");
        }
    }
});