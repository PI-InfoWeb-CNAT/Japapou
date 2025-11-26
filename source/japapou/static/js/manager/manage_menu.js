document.addEventListener('DOMContentLoaded', function() {

  // Seleciona o modal de edição
  const editDialog = document.getElementById('editar-prato');

  // Adiciona o evento de clique para TODOS os botões de edição
  document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function() {
      // Pega o ID do prato do atributo 'plate-id' do botão
      const plateId = this.getAttribute('plate-id');
      
      // Constrói a URL correta para buscar os dados do prato
      //    A URL deve corresponder ao que está em 'manager_urls.py'
      //const url = `/plates/${plateId}/json/`;
      const url = this.getAttribute('data-url');
      console.log(url);

      const nextPage = this.getAttribute('data-next-page');

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
          
          const redirectInput = form.querySelector('#redirect-after-update');
          if (redirectInput) { // Verifica se o campo existe antes de tentar preencher
              redirectInput.value = nextPage;
          }
        
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

  const cards = document.querySelectorAll(".product-card");

  cards.forEach(card => {
    // 1. Lemos a média (que será 0 se não houver avaliações)
    const media = parseFloat(card.dataset.media);
    
    // 2. Selecionamos todas as 5 estrelas DENTRO deste card
    const estrelas = card.querySelectorAll(".star");

    // 3. Iteramos por todas as 5 estrelas (index de 0 a 4)
    estrelas.forEach((star, index) => {
      
      
      // Se o 'index' da estrela for MAIOR ou IGUAL à média,
      // ela deve ser pintada de cinza (inativa).
      //
      // Exemplo (Média = 0):
      // Index 0: (0 >= 0) -> Adiciona .star-inactive (Cinza)
      // ... todas ficam cinza
      
      if (index >= media) {
        star.classList.add("star-inactive");
        // console.log(index)
      }
      
      // As estrelas ativas (abaixo da média) simplesmente
      // não recebem a classe .star-inactive e ficam com a
      // cor amarela padrão que definimos no CSS.
    });
  });

  const photoPreview = document.getElementById('edit-photo-preview');
  const photoInput = document.getElementById('edit-photo-input');
  const photoContainer = document.getElementById('image-file-edit-container');

  // Apenas executa se os elementos existirem (boa prática)
  if (photoPreview && photoInput && photoContainer) {
  
      // 1. Permite clicar na imagem para abrir o seletor de ficheiros
      // (O clique no #upload-label já funciona via HTML/Label, mas este melhora a usabilidade)
      photoContainer.addEventListener('click', () => {
          photoInput.click();
      });
    
      // 2. Pré-visualização Imediata da Nova Foto
      photoInput.addEventListener('change', function() {
          if (this.files && this.files[0]) {
              const reader = new FileReader(); 
              
              reader.onload = function(e) {
                  // Atualiza o atributo 'src' da imagem com a nova foto
                  photoPreview.src = e.target.result;
                  photoPreview.style.display = 'block'; 
              };
              
              reader.readAsDataURL(this.files[0]);
          }
      });
  }

  function getOptionTextWidth(optionElement) {
    // função para pegar o tamanho width e um texto para usar como regua

    const optionText = optionElement.textContent;
    
    // Tenta encontrar o elemento régua, se já existir
    let ruler = document.querySelector('.text-ruler');

    // Se a régua não existir, cria e a adiciona ao corpo do documento
    if (!ruler) {
        ruler = document.createElement('span');
        ruler.classList.add('text-ruler');
        document.body.appendChild(ruler);
    }
    
    // 2. Define o texto da opção na régua
    ruler.textContent = optionText;
    
    // 3. Mede a largura do elemento régua
    // getBoundingClientRect().width é a mais precisa.
    const larguraCalculada = ruler.getBoundingClientRect().width;
    
    // 4. (Opcional) Remove a régua do DOM após a medição (ou a reutiliza para eficiência)
    // Se você for medir várias vezes, é melhor mantê-la e reutilizá-la.
    // document.body.removeChild(ruler); 

    // Retorna a largura calculada, adicionando uma pequena margem (ex: 5px)
    return larguraCalculada + 5; 
  }

  const selectMenu = document.getElementById('id_field');
  const selectPeriod = document.getElementById('id_period_field');

  const formSelectMenu = document.getElementById('form-select-menu');
  const formPeriodMenu = document.getElementById('period-form');

  // console.log(selectMenu);
  // console.log(selectPeriod);
  // console.log(formPeriodMenu);
  // console.log(formSelectMenu);

  const valorAtual = selectMenu.options[selectMenu.selectedIndex];

  function copiarLargura() {
    // função que copia largura do nome do menu para evitar que
    // caso o nome seja muito grande fique passando
    const valorAtual = selectMenu.options[selectMenu.selectedIndex];
    

    let larguraValorAtual = getOptionTextWidth(valorAtual);
    console.log("Largura:", (larguraValorAtual));
    
    formSelectMenu.style.width = (larguraValorAtual+130) + "px";

  };
  console.log(getOptionTextWidth(valorAtual))
  copiarLargura()
});


  const addPratoExisten = document.getElementById("addpratoexistentbtn");
  const addNovoPrato = document.getElementById("addnovopratobtn");
  const modalNovoCardapio = document.getElementById("novo-cardapio");

  const modalNovoPrato = document.getElementById("novo-prato");
  const modalAddNovoPrato = document.getElementById("criar-prato");

  modalNovoPrato.addEventListener("click", function (event) {
    if (event.target === modalNovoPrato) {
      modalNovoPrato.close();
    }
  });

  modalNovoCardapio.addEventListener("click", function (event) {
    if (event.target === modalNovoCardapio) {
      modalNovoCardapio.close();
    }
  });

  addPratoExisten.addEventListener("click", () => {
    modalNovoPrato.close();
  });

  addNovoPrato.addEventListener("click", () => {
    modalNovoPrato.close();
    modalAddNovoPrato.showModal();
});


