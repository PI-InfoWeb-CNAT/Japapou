// manage_plates.js
document.addEventListener('DOMContentLoaded', function() {
  // Seleciona o modal de edição
  const editDialog = document.getElementById('editar-prato');

  // Adiciona o evento de clique para TODOS os botões de edição
  document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function() {
      // 1. Pega o ID do prato do atributo 'plate-id' do botão
      const plateId = this.getAttribute('plate-id');
      
      // 2. Constrói a URL correta para buscar os dados do prato
      //    A URL deve corresponder ao que está em 'manager_urls.py'
      //const url = `/plates/${plateId}/edit/`;
      const url = this.getAttribute('data-url');

      // 3. Faz a requisição (fetch) para o backend
      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('A requisição falhou! Status: ' + response.status);
          }
          return response.json(); // Converte a resposta para JSON
        })
        .then(data => {
          // 4. Preenche o formulário no modal de edição com os dados recebidos
          const form = document.getElementById('form-editar-prato');

          // Define a action do formulário para a URL de update correta
          form.action = `/manager/plates/${data.id}/update/`; // Vamos criar essa URL no passo 3

          // Preenche os campos de texto e número
          form.querySelector('#edit-name').value = data.name;
          form.querySelector('#edit-description').value = data.description;
          form.querySelector('#edit-price').value = data.price;
          
          // Mostra a imagem atual do prato
          const photoPreview = form.querySelector('#edit-photo-preview');
          if (data.photo_url) {
            photoPreview.src = data.photo_url;
            photoPreview.style.display = 'block';
          } else {
            photoPreview.style.display = 'none';
          }

          // Seleciona os menus corretos no campo 'select multiple'
          const menuSelect = form.querySelector('#id_menus'); // O Django gera o ID 'id_menus'
          Array.from(menuSelect.options).forEach(option => {
            // Converte o valor da opção para número para comparação
            option.selected = data.menus.includes(parseInt(option.value));
          });
          
          // 5. Abre o modal
          editDialog.showModal();
        })
        .catch(error => {
          console.error("Houve um erro ao buscar os dados do prato:", error);
          alert("Não foi possível carregar os dados para edição.");
        });
    });
  });
  const deleteDialog = document.getElementById('excluir-prato');
  const deleteForm = document.getElementById('form-excluir-prato');

  document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function() {
      // 1. Pega o ID do prato do botão clicado
      const plateId = this.getAttribute('plate-id');

      // 2. Monta a URL de action para o formulário de exclusão
      deleteForm.action = `/manager/plates/${plateId}/delete/`;

      // 3. Abre o modal de confirmação
      deleteDialog.showModal();
    });
  });
});