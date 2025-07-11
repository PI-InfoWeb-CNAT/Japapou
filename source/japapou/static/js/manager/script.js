// Espera todo o conteúdo da página ser carregado para executar o código
document.addEventListener('DOMContentLoaded', () => {

    // 1. Seleciona os elementos do card com os quais vamos interagir
    const productCard = document.querySelector('.product-card');
    const removeButton = document.querySelector('.remove-button');
    const deleteButton = document.querySelector('.delete-button');
    const editButton = document.querySelector('.edit-button');

    // Função para remover o card com uma animação suave
    function handleRemoveCard() {
        console.log('Botão de remover/deletar clicado!');
        // Adiciona uma classe para animar a saída do card
        productCard.style.transition = 'transform 0.5s ease, opacity 0.5s ease';
        productCard.style.transform = 'scale(0.8)';
        productCard.style.opacity = '0';

        // Espera a animação terminar para remover o elemento da página
        setTimeout(() => {
            productCard.remove();
        }, 500); // 500 milissegundos, o mesmo tempo da transição
    }

    // 2. Adiciona "escutadores de eventos" aos botões de remoção
    // Quando o botão "REMOVER" for clicado, a função handleRemoveCard será executada.
    removeButton.addEventListener('click', handleRemoveCard);
    
    // O mesmo para o botão "X"
    deleteButton.addEventListener('click', handleRemoveCard);

    // 3. Adiciona um evento para o botão de edição
    // Quando o botão de "lápis" for clicado, ele mostrará um alerta simples.
    editButton.addEventListener('click', () => {
        alert('Você clicou no botão de editar o produto!');
    });

});