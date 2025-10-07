document.addEventListener("DOMContentLoaded", function () {
	const editIcons = document.querySelectorAll(".edit-icon");
  
	editIcons.forEach((icon) => {
	  icon.addEventListener("click", function (event) {
		event.preventDefault();
  
		const container = this.closest(".value-with-icon");
		const span = container.querySelector("span");
  
		if (!span || container.querySelector("input")) return;
  
		const field = span.dataset.field;
		const userId = span.dataset.id;
		const currentValue = span.textContent.trim();
  
		const input = document.createElement("input");
		input.type = "text";
		input.value = currentValue;
		input.className = "temp-edit-input";
  
		container.replaceChild(input, span);
		input.focus();
  
		async function saveEdit() {
		  const newValue = input.value.trim();
  
		  // Cria o novo <span>
		  const newSpan = document.createElement("span");
		  newSpan.textContent = newValue;
		  newSpan.dataset.field = field;
		  newSpan.dataset.id = userId;
		  newSpan.className = "editable-span";
		  container.replaceChild(newSpan, input);
  
		  // Envia o dado via fetch (AJAX)
		  try {
			const response = await fetch("/profile/update_user/", {
			  method: "POST",
			  headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": getCSRFToken(),
			  },
			  body: JSON.stringify({
				id: userId,
				field: field,
				value: newValue,
			  }),
			});
  
			const result = await response.json();
			if (!response.ok || result.status !== "ok") {
			  alert("Erro ao salvar!");
			  console.log(result);
			}
		  } catch (err) {
			console.error("Erro:", err);
		  }
		}
  
		input.addEventListener("blur", saveEdit);
		input.addEventListener("keydown", function (e) {
		  if (e.key === "Enter") input.blur();
		});
	  });
	});
  
	const fileInput = document.getElementById("fileInput");
	const previewImage = document.getElementById("previewImage");
  
	if (fileInput && previewImage) {
	  fileInput.addEventListener("change", (event) => {
		const file = event.target.files[0];
		if (file) {
		  const formData = new FormData();
		  formData.append("foto", file);
  
		  // Você pode enviar o ID do usuário se necessário
		  formData.append("id", "{{ user.id }}");
  
		  fetch("/profile/update_photo/", {
			method: "POST",
			headers: {
			  "X-CSRFToken": getCSRFToken(),
			},
			body: formData,
		  })
			.then((response) => response.json())
			.then((data) => {
			  if (data.status === "ok") {
				previewImage.src = data.nova_foto_url;
				// Se quiser, chame updateAlt() aqui, mas defina ela antes
			  } else {
				alert("Erro ao enviar imagem");
			  }
			})
			.catch((error) => {
			  console.error("Erro:", error);
			});
  
		  // Se quiser mostrar preview local ANTES do upload, descomente:
		  /*
		  const reader = new FileReader();
		  reader.onload = (e) => {
			previewImage.src = e.target.result;
		  };
		  reader.readAsDataURL(file);
		  */
		}
	  });
	}
  
	function getCSRFToken() {
	  return document.querySelector('[name=csrfmiddlewaretoken]').value;
	}
  });
  