document.addEventListener("DOMContentLoaded", () => {
	console.log("manage_profile.js carregado ✅");

	function getCSRFToken() {
		const token = document.querySelector('[name=csrfmiddlewaretoken]');
		return token ? token.value : "";
	}

	// 🔹 EDIÇÃO INLINE VIA BOTÃO
	const editButtons = document.querySelectorAll(".edit-icon");

	editButtons.forEach((btn) => {
		btn.addEventListener("click", (e) => {
			e.preventDefault();
			const targetId = btn.dataset.edit;
			const editable = document.getElementById(targetId);
			if (!editable) return;

			const currentValue = editable.textContent.trim();

			// Cria input temporário
			const input = document.createElement("input");
			input.type = "text";
			input.value = currentValue;
			input.className = "temp-edit-input";

			editable.replaceWith(input);
			input.focus();

			async function saveEdit() {
				let newValue = input.value.trim();

				// 🔹 Converte data_nascimento para formato ISO
				if (editable.dataset.field === "data_nascimento") {
					const parts = newValue.split("/");
					if (parts.length === 3) {
						// dd/mm/yyyy -> yyyy-mm-dd
						newValue = `${parts[2]}-${parts[1].padStart(2, "0")}-${parts[0].padStart(2, "0")}`;
					}
				}

				// Restaura o span
				input.replaceWith(editable);
				editable.textContent = newValue;

				// Envia via AJAX
				try {
					const response = await fetch("/manager/profile/update_user/", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": getCSRFToken(),
						},
						body: JSON.stringify({
							id: editable.dataset.id,
							field: editable.dataset.field,
							value: newValue,
						}),
					});

					const result = await response.json();
					if (!response.ok || result.status !== "ok") {
						alert("Erro ao salvar! " + (result.mensagem || ""));
						console.log(result);
					}
				} catch (err) {
					console.error("Erro:", err);
				}
			}

			input.addEventListener("blur", saveEdit);
			input.addEventListener("keydown", (e) => {
				if (e.key === "Enter") input.blur();
			});
		});
	});

	// 🔹 UPLOAD DE FOTO
	const fileInput = document.getElementById("fileInput");
	const previewImage = document.getElementById("previewImage");

	if (fileInput && previewImage) {
		fileInput.addEventListener("change", async (event) => {
			const file = event.target.files[0];
			if (!file) return;

			const formData = new FormData();
			formData.append("foto", file);
			formData.append("id", "{{ user.id }}"); // Django template

			try {
				const response = await fetch("/manager/profile/update_photo/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(),
					},
					body: formData,
				});

				const data = await response.json();
				if (data.status === "ok") {
					// Atualiza o preview da imagem
					previewImage.src = data.nova_foto_url + "?t=" + new Date().getTime(); // força cache buster
				} else {
					alert("Erro ao enviar imagem: " + (data.mensagem || ""));
				}
			} catch (error) {
				console.error("Erro ao enviar imagem:", error);
			}
		});
	}
});
