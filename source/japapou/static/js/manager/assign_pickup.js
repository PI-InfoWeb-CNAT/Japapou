document.addEventListener('DOMContentLoaded', () => {

  // Coverflow
  const slides = document.querySelectorAll('.slide');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  let current = slides.length >= 3 ? 1 : 0;

  function updateSlides() {
    slides.forEach((slide, i) => {
      const offset = i - current;
      const absOffset = Math.abs(offset);
      const prato = slide.querySelector('.prato');
      const especificacao = slide.querySelector('.especificacao');
      const circ_2 = slide.querySelector('.circ-2>p');
      const circ_1 = slide.querySelector('.circ-1');
      const maxVisible = 2;

      if (absOffset > maxVisible) {
        slide.style.opacity = '0';
        slide.style.pointerEvents = 'none';
        slide.style.transform = 'scale(0.5) translateX(0)';
        slide.style.zIndex = 0;
        return;
      }

      slide.style.opacity = '1';
      slide.style.pointerEvents = 'auto';
      slide.style.zIndex = 10 - absOffset;

      const slideWidth = slides[0].offsetWidth + 20;

      if (offset === 0) {
        slide.style.transform = 'translateX(0) scale(1)';
        if (prato) prato.style.color = 'white';
        if (especificacao) especificacao.style.backgroundColor = 'var(--azul-mais-escuro)';
        if (circ_2) circ_2.style.color = 'var(--azul-mais-escuro)';
        if (circ_1) circ_1.style.backgroundColor = 'var(--azul-mais-escuro)';
      } else {
        slide.style.transform = `translateX(${offset * slideWidth}px) scale(0.7)`;
        if (prato) prato.style.color = 'white';
        if (especificacao) especificacao.style.backgroundColor = 'var(--vermelho)';
        if (circ_2) circ_2.style.color = 'var(--vermelho)';
        if (circ_1) circ_1.style.backgroundColor = 'var(--vermelho)';
      }
    });
  }

  function goNext() { if (current < slides.length - 1) { current++; updateSlides(); } }
  function goPrev() { if (current > 0) { current--; updateSlides(); } }

  prevBtn.addEventListener('click', goPrev);
  nextBtn.addEventListener('click', goNext);
  updateSlides();

  // Confirmar retirada
  const confirmBtn = document.getElementById('button-3');
  if (!confirmBtn) return;

  confirmBtn.addEventListener('click', async () => {
    if (confirmBtn.classList.contains('confirmed')) return;

    const container = document.getElementById('detalhes-retirada');
    const orderId = container.dataset.orderId;
    const csrf = container.dataset.csrf;

    try {
      const response = await fetch(`/manager/confirm_pickup/${orderId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (data.status === 'ok') {
        confirmBtn.innerHTML = `<h4>Retirada registrada (${data.pickup_date})</h4>`;
        confirmBtn.style.backgroundColor = '#3bb33b';
        confirmBtn.classList.add('confirmed');
      } else {
        alert('Erro ao registrar retirada.');
      }
    } catch (error) {
      console.error(error);
      alert('Erro de conexão.');
    }
  });

});