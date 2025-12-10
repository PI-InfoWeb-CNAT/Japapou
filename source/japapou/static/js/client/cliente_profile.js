document.addEventListener("DOMContentLoaded", () => {
	console.log("client_profile.js carregado ✅");

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
				let newValue = input.value.trim(); // O valor atual é YYYY-MM-DD (do input type="date")

				let valueToSend = newValue; // Mantém no formato YYYY-MM-DD para o backend (padrão Django)

				// 🔹 Converte data_nascimento para EXIBIÇÃO no frontend, se não estiver vazio
				if (editable.dataset.field === "data_nascimento") {
					
					// Converte yyyy-mm-dd (que está em newValue) para dd/mm/yyyy para exibição
					if (newValue) {
						const parts = newValue.split("-");
						if (parts.length === 3) {
							// Formato de exibição: dd/mm/yyyy
							const formatted = `${parts[2]}/${parts[1]}/${parts[0]}`;
							editable.textContent = formatted;
						}
					} else {
						// Data vazia → exibe "—"
						editable.textContent = "—";
					}
					
				} else {
					// Senha → não mostrar valor
					if (editable.dataset.field === "senha") {
						editable.textContent = "**************";
					}
					// Outros campos → valor direto
					else {
						editable.textContent = newValue || "—";
					}
				}
				
				// Restaura o span original
				input.replaceWith(editable);


				// Envia via AJAX
				try {
					const response = await fetch("/client/profile/update_user/", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": getCSRFToken(),
						},
						body: JSON.stringify({
							id: editable.dataset.id,
							field: editable.dataset.field,
							// 🚨 CORREÇÃO PRINCIPAL: Envia o valor YYYY-MM-DD (valueToSend)
							value: valueToSend, 
						}),
					});

					const result = await response.json();
					if (response.ok && result.status === "ok") {
						// ⭐ SUCESSO na edição inline
						showStatusToast('Suas informações foram alteradas com sucesso!', true);
					} else {
						// ⭐ ERRO na edição inline
						showStatusToast("Erro ao salvar! " + (result.mensagem || "Verifique o console."), false);
						console.log(result);
					}
				} catch (err) {
					// ⭐ ERRO na requisição
					showStatusToast("Erro de conexão ao tentar salvar.", false);
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
				const response = await fetch("/client/profile/update_photo/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(),
					},
					body: formData,
				});

				const data = await response.json();
				if (data.status === "ok") {
					previewImage.src = data.nova_foto_url + "?t=" + new Date().getTime();
					// ⭐ SUCESSO no upload de foto
					showStatusToast('Foto de perfil alterada com sucesso!', true);
				} else {
					// ⭐ ERRO no upload de foto
					showStatusToast("Erro ao enviar imagem: " + (data.mensagem || "Verifique o console."), false);
				}
			} catch (error) {
				// ⭐ ERRO na requisição
				showStatusToast("Erro de conexão ao tentar fazer upload.", false);
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
				const response = await fetch("/client/profile/update_photo/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(),
					},
					body: formData,
				});

				const data = await response.json();
				if (data.status === "ok") {
					// A constante 'defaultImagePath' está definida no profile.html
					previewImage.src = defaultImagePath || "/static/imgs/manager/profile.png"; 
					// ⭐ SUCESSO na remoção de foto
					showStatusToast('Foto de perfil removida com sucesso!', true);
				} else {
					// ⭐ ERRO na remoção de foto
					showStatusToast("Erro ao remover a foto: " + (data.mensagem || "Verifique o console."), false);
				}
			} catch (error) {
				// ⭐ ERRO na requisição
				showStatusToast("Erro de conexão ao tentar remover a foto.", false);
				console.error("Erro ao remover a foto:", error);
			}
		});
	}
});