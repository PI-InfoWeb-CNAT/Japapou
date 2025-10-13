  const slides = document.querySelectorAll('.slide');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  let current = 2;

  function updateSlides() {
  slides.forEach((slide, i) => {
    const offset = i - current;
    const absOffset = Math.abs(offset);
    const prato = slide.querySelector('.prato');
    const especificacao = slide.querySelector('.especificacao');
    const circ_2 = slide.querySelector('.circ-2>p')
    const circ_1 = slide.querySelector('.circ-1')

    if (absOffset > 1) {
      slide.style.opacity = '0';
      slide.style.pointerEvents = 'none';
      slide.style.transform = 'scale(0.5) translateX(0)';
      slide.style.zIndex = 0;

      if (prato) prato.style.color = 'var(--azul-mais-escuro)';
      if(especificacao) especificacao.style.backgroundColor = 'white';
      if(circ_2) circ_2.style.color = 'var(--vermelho)';
      if(circ_1) circ_1.style.backgroundColor = 'var(--vermelho)';

      return;
    }

    slide.style.opacity = '1';
    slide.style.pointerEvents = 'auto';
    slide.style.zIndex = 10 - absOffset;

    if (offset === 0) {
      slide.style.transform = 'translateX(0) scale(1)';
      if (prato) prato.style.color = 'white';
      if(especificacao) especificacao.style.backgroundColor = 'var(--azul-mais-escuro)';
      if(circ_2) circ_2.style.color = 'var(--azul-mais-escuro)';
      if(circ_1) circ_1.style.backgroundColor = 'var(--azul-mais-escuro)';
    } else {
      slide.style.transform = `
        translateX(${offset * 400}px)
        rotateY(0deg)
        scale(0.7)
      `;
      if (prato) prato.style.color = 'white';
      if(especificacao) especificacao.style.backgroundColor = 'var(--vermelho)';
      if(circ_1) circ_1.style.color = 'var(--vermelho)';
      if(circ_1) circ_1.style.backgroundColor = 'var(--vermelho)';
    }
  });
}

  function goNext() {
    if (current < slides.length - 1) {
      current++;
      updateSlides();
    }
  }

  function goPrev() {
    if (current > 0) {
      current--;
      updateSlides();
    }
  }

  prevBtn.addEventListener('click', goPrev);
  nextBtn.addEventListener('click', goNext);

  // inicia
  updateSlides();

function toggleMenu() {
	const menu = document.getElementById("sideMenu");
	const burger = document.querySelector(".hamburger");
	menu.classList.toggle("active");
	burger.classList.toggle("active");
}
