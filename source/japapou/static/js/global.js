const header = document.getElementById("header");
let lastScrollY = window.scrollY;

window.addEventListener("scroll", () => {
	if (window.scrollY < lastScrollY) {
		// Scrolling up
		header.classList.remove("header-hidden");
	} else {
		// Scrolling down
		header.classList.add("header-hidden");
	}
	lastScrollY = window.scrollY;
});

function toggleMenu() {
	const menu = document.getElementById("sideMenu");
	const burger = document.querySelector(".hamburger");
	menu.classList.toggle("active");
	burger.classList.toggle("active");
}
