document.addEventListener("DOMContentLoaded", function () {
    const editIcons = document.querySelectorAll(".edit-icon");

    editIcons.forEach(icon => {
        icon.addEventListener("click", function (event) {
            event.preventDefault(); // Impede comportamento padrão do link ou botão

            const container = this.closest(".value-with-icon");
            const span = container.querySelector("span");

            if (!span) return;

            const currentValue = span.textContent.trim();

            // Evita criar múltiplos inputs se já estiver editando
            if (container.querySelector("input")) return;

            // Cria o campo de input
            const input = document.createElement("input");
            input.type = "text";
            input.value = currentValue;
            input.className = "temp-edit-input";

            // Substitui o span pelo input
            container.replaceChild(input, span);
            input.focus();

            // Função para restaurar o span com novo texto
            function restoreSpan() {
                const newSpan = document.createElement("span");
                newSpan.textContent = input.value || currentValue;
                container.replaceChild(newSpan, input);
            }

            // Quando o campo perde o foco
            input.addEventListener("blur", restoreSpan);

            // Quando o usuário pressiona Enter
            input.addEventListener("keydown", function (e) {
                if (e.key === "Enter") {
                    input.blur(); // Dispara blur para restaurar o texto
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
  const previewImage = document.getElementById('previewImage');
  const removeImageBtn = document.getElementById('removeImageBtn');
  const fileInput = document.getElementById('fileInput');

  // Define alt vazio só se for a imagem padrão
  function updateAlt() {
    if (previewImage.src.includes(defaultImagePath)) {
      previewImage.alt = '';  // limpa alt pra não mostrar texto "por trás"
    } else {
      previewImage.alt = 'Foto de perfil'; // alt normal pra imagem customizada
    }
  }

  updateAlt();

  fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImage.src = e.target.result;
        updateAlt();
      };
      reader.readAsDataURL(file);
    }
  });

  removeImageBtn.addEventListener('click', () => {
    previewImage.src = defaultImagePath;
    updateAlt();
    fileInput.value = '';
  });
});
