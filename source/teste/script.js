document.addEventListener('DOMContentLoaded', () => {
    // 1. Elementos da DOM
    const gridContainer = document.getElementById('cards-grid');
    const detailContainer = document.getElementById('card-detail');
    const backButton = document.getElementById('back-to-grid');
    const newCardButton = document.getElementById('new-card-button');

    // Elementos do Modal de Exclusão
    const deleteModal = document.getElementById('deleteModal');
    const deleteNameSpan = document.getElementById('delete-name');
    const cancelDeleteBtn = document.getElementById('cancel-delete');
    const confirmDeleteBtn = deleteModal.querySelector('.btn--confirm-delete');
    let cardToDelete = null; // Armazena temporariamente o card a ser excluído

    // Elementos do Modal de Adição
    const addModal = document.getElementById('addModal');
    const cancelAddBtn = document.getElementById('cancel-add');
    const addForm = document.getElementById('add-form');

    // 2. Lógica principal de cliques na grade
    gridContainer.addEventListener('click', (event) => {
        const target = event.target;
        const cardEntregador = target.closest('.card--entregador');
        
        // --- AÇÃO 1: ABRIR MODAL DE EXCLUIR ---
        if (target.classList.contains('btn--excluir')) {
            event.stopPropagation(); // Impede que o clique no botão ative o detalhe
            
            if (cardEntregador) {
                cardToDelete = cardEntregador;
                
                // Pega o nome do entregador para exibir no modal
                const name = cardEntregador.querySelector('.card__name').textContent;
                deleteNameSpan.textContent = name;
                
                deleteModal.style.display = 'flex'; // Mostra o modal
            }
            return;
        }

        // --- AÇÃO 2: ABRIR MODAL DE ADICIONAR ---
        if (target.closest('#new-card-button')) {
            addModal.style.display = 'flex'; // Mostra o modal de adição
            return;
        }
        
        // --- AÇÃO 3: DETALHAR CARD (clique no corpo do card) ---
        if (cardEntregador) {
            console.log(`Card ID ${cardEntregador.dataset.id} clicado. Indo para Detalhe.`);
            gridContainer.style.display = 'none';
            detailContainer.style.display = 'block';
        }
    });

    // 3. Lógica dos Modais

    // Excluir - CONFIRMAR
    confirmDeleteBtn.addEventListener('click', () => {
        if (cardToDelete) {
            cardToDelete.remove();
            console.log('Card excluído após confirmação do modal.');
            cardToDelete = null;
            deleteModal.style.display = 'none'; // Esconde o modal
        }
    });

    // Cancelar - EXCLUIR
    cancelDeleteBtn.addEventListener('click', () => {
        cardToDelete = null;
        deleteModal.style.display = 'none';
    });

    // Cancelar - ADICIONAR
    cancelAddBtn.addEventListener('click', () => {
        addModal.style.display = 'none';
        addForm.reset(); // Limpa o formulário
    });

    // Adicionar - CONFIRMAR (Submissão do formulário)
    addForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        // 1. Coleta os dados do formulário
        const nome = document.getElementById('entregador-nome').value;
        const avaliacao = parseFloat(document.getElementById('entregador-avaliacao').value);
        const newCardId = Date.now();

        // 2. Cria o novo HTML do Card
        const newCardHTML = `
            <div class="card card--entregador" data-id="${newCardId}">
                <img src="https://i.ibb.co/9vjYn5x/modelo.jpg" alt="${nome}" class="card__image">
                <h3 class="card__name">${nome}</h3>
                <div class="card__rating">
                    ${generateStarHTML(avaliacao)}
                </div>
                <div class="card__actions">
                    <button class="btn btn--excluir">Excluir</button>
                    <button class="btn btn--editar">Editar</button>
                </div>
            </div>
        `;
        
        // 3. Insere o novo card antes do botão '+'
        newCardButton.insertAdjacentHTML('beforebegin', newCardHTML);
        
        // 4. Limpa e fecha o modal
        addModal.style.display = 'none';
        addForm.reset();
        console.log(`Novo entregador '${nome}' adicionado.`);
    });
    
    /**
     * Função auxiliar para gerar estrelas com base na avaliação
     * @param {number} rating - A nota de avaliação (ex: 4.5)
     * @returns {string} - O HTML dos ícones de estrela
     */
    function generateStarHTML(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                // Estrela cheia
                stars += '<span class="star">&#9733;</span>';
            } else if (i - rating < 1 && i - rating > 0) {
                // Simula meia estrela (usando a classe half-star com opacidade 0.5 no CSS)
                stars += '<span class="star half-star">&#9733;</span>';
            } else {
                // Estrela vazia (usando a classe half-star com opacidade 0.2 no CSS)
                stars += '<span class="star half-star" style="opacity: 0.2;">&#9733;</span>';
            }
        }
        return stars;
    }

    // 4. Transição de volta para a tela de Grade
    backButton.addEventListener('click', () => {
        detailContainer.style.display = 'none';
        gridContainer.style.display = 'grid';
    });
    
    // 5. Fechar modal ao clicar fora dele
    window.addEventListener('click', (event) => {
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
            cardToDelete = null;
        }
        if (event.target === addModal) {
            addModal.style.display = 'none';
            addForm.reset();
        }
    });
});