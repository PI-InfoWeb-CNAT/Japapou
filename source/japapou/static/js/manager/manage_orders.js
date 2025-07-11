function toggleDetalhes(button) {
	const detalhes = button.nextElementSibling;
	if (detalhes.style.display === "block") {
		detalhes.style.display = "none";
	} else {
		detalhes.style.display = "block";
	}
}

// Lightbox funcional
const images = document.querySelectorAll(".pedido-imagens img");
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

images.forEach((img) => {
	img.addEventListener("click", () => {
		lightboxImg.src = img.src;
		lightbox.classList.add("active");
	});
});

lightbox.addEventListener("click", () => {
	lightbox.classList.remove("active");
	lightboxImg.src = "";
});
