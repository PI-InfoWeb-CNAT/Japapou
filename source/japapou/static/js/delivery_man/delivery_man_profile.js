document.addEventListener("DOMContentLoaded", () => {
	console.log("delivery_man_profile.js carregado ✅");

	// 🔹 Função utilitária para pegar o token CSRF
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

			let currentValue = editable.textContent.trim();

			// Cria input temporário
			const input = document.createElement("input");

			// 🔸 Se for senha → campo vazio, tipo password
			if (editable.dataset.field === "senha") {
				input.type = "password";
				input.value = "";
				input.placeholder = "Digite a nova senha";
			}
			// 🔸 Se for data de nascimento → input date
			else if (editable.dataset.field === "data_nascimento") {
				input.type = "date";

				if (currentValue && currentValue !== "None") {
					// Converte dd/mm/yyyy → yyyy-mm-dd
					const parts = currentValue.split("/");
					if (parts.length === 3) {
						input.value = `${parts[2]}-${parts[1].padStart(2, "0")}-${parts[0].padStart(2, "0")}`;
					}
				} else {
					input.value = "";
				}
			}
			// 🔸 Outros campos → input texto normal
			else {
				input.type = "text";
				input.value = currentValue;
			}

			input.className = "temp-edit-input";
			editable.replaceWith(input);
			input.focus();

			async function saveEdit() {
				let newValue = input.value.trim();

				// 🔹 Converte data_nascimento antes de enviar
				if (editable.dataset.field === "data_nascimento" && newValue) {
					// yyyy-mm-dd → dd/mm/yyyy para exibição
					const parts = newValue.split("-");
					if (parts.length === 3) {
						const formatted = `${parts[2]}/${parts[1]}/${parts[0]}`;
						newValue = formatted;
					}
				}

				// Restaura o span original
				input.replaceWith(editable);

				// Senha → não mostrar valor
				if (editable.dataset.field === "senha") {
					editable.textContent = "**************";
				}
				// Data vazia → exibe "—"
				else if (editable.dataset.field === "data_nascimento" && !newValue) {
					editable.textContent = "—";
				}
				// Outros campos → valor direto
				else {
					editable.textContent = newValue || "—";
				}

				// Envia via AJAX
				try {
					const response = await fetch("/delivery_man/profile/update_user/", {
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
	const removeImageBtn = document.getElementById("removeImageBtn");
	const fotoContainer = document.querySelector(".foto-container");
	const userId = fotoContainer ? fotoContainer.dataset.userId : null;

	if (fileInput && previewImage && userId) {
		fileInput.addEventListener("change", async (event) => {
			const file = event.target.files[0];
			if (!file) return;

			const formData = new FormData();
			formData.append("foto", file);
			formData.append("id", userId);

			try {
				const response = await fetch("/delivery_man/profile/update_photo/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(),
					},
					body: formData,
				});

				const data = await response.json();
				if (data.status === "ok") {
					previewImage.src = data.nova_foto_url + "?t=" + new Date().getTime();
				} else {
					alert("Erro ao enviar imagem: " + (data.mensagem || ""));
				}
			} catch (error) {
				console.error("Erro ao enviar imagem:", error);
			}
		});
	}

	// 🔹 REMOVER FOTO
	if (removeImageBtn && previewImage && userId) {
		removeImageBtn.addEventListener("click", async () => {
			if (!confirm("Deseja realmente remover sua foto de perfil?")) return;

			const formData = new FormData();
			formData.append("remover", "true");
			formData.append("id", userId);

			try {
				const response = await fetch("/delivery_man/profile/update_photo/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(),
					},
					body: formData,
				});

				const data = await response.json();
				if (data.status === "ok") {
					previewImage.src = "/static/imgs/manager/profile.png";
				} else {
					alert("Erro ao remover a foto: " + (data.mensagem || ""));
				}
			} catch (error) {
				console.error("Erro ao remover a foto:", error);
			}
		});
	}
});
