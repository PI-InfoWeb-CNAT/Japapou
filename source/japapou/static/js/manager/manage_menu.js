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
