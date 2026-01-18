// manage_plates.js

// Função auxiliar para obter o token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Lógica do Modal de Edição (Preencher dados e abrir) ---
    const editDialog = document.getElementById('editar-prato');

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const plateId = this.getAttribute('plate-id');
            const url = this.getAttribute('data-url');
            const nextPage = this.getAttribute('data-next-page');

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('A requisição falhou! Status: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    const form = document.getElementById('form-editar-prato');
                    
                    // Atualiza a action do form
                    form.action = `/manager/plates/${data.id}/update/`;

                    // Preenche os campos
                    form.querySelector('#edit-name').value = data.name;
                    form.querySelector('#edit-description').value = data.description;
                    form.querySelector('#edit-price').value = data.price;

                    // Mostra a imagem atual
                    const photoPreview = form.querySelector('#edit-photo-preview');
                    if (data.photo_url) {
                        photoPreview.src = data.photo_url;
                        photoPreview.style.display = 'block';
                    } else {
                        photoPreview.style.display = 'none';
                    }

                    // Seleciona os menus associados
                    const menuSelect = form.querySelector('#id_menus');
                    if (menuSelect) {
                        Array.from(menuSelect.options).forEach(option => {
                            option.selected = data.menus.includes(parseInt(option.value));
                        });
                    }

                    // Define o redirecionamento
                    const redirectInput = form.querySelector('#redirect-after-update');
                    if (redirectInput) {
                        redirectInput.value = nextPage;
                    }

                    editDialog.showModal();
                })
                .catch(error => {
                    console.error("Houve um erro ao buscar os dados do prato:", error);
                    alert("Não foi possível carregar os dados para edição.");
                });
        });
    });

    // --- 2. Lógica das Estrelas (Avaliação) ---
    const cards = document.querySelectorAll(".product-card");
    cards.forEach(card => {
        const media = parseFloat(card.dataset.media);
        const estrelas = card.querySelectorAll(".star");
        estrelas.forEach((star, index) => {
            if (index >= media) {
                star.classList.add("star-inactive");
            }
        });
    });

    // --- 3. Lógica de Pré-visualização da Imagem (Upload) ---
    const photoPreview = document.getElementById('edit-photo-preview');
    const photoInput = document.getElementById('edit-photo-input');
    const photoContainer = document.getElementById('image-file-edit-container');

    if (photoPreview && photoInput && photoContainer) {
        // Clicar na imagem/container abre o seletor de ficheiros
        photoContainer.addEventListener('click', () => {
            photoInput.click();
        });

        // Quando o ficheiro muda, atualiza a imagem no modal
        photoInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    photoPreview.src = e.target.result;
                    photoPreview.style.display = 'block';
                };

                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});

// Nota: Removi todo o código referente a "Novo Menu", "Filtros de Data" e "Botões de Prato Existente"
// pois esses elementos não existem na página manager_plates.html e causavam erro.