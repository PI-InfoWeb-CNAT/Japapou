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
  updateSlides();

  // Modal
  const modal = document.getElementById('modalDeliveryMan');
  const closeModal = document.getElementById('closeModal');
  const assignBtn = document.getElementById('assignDeliveryManBtn');

  const openModalBtns = document.querySelectorAll('.assign-delivery-btn');
  openModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modal.style.display = 'block';
    });
  });

  closeModal.addEventListener('click', () => modal.style.display = 'none');
  window.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = 'none'; });

  // Atribuir entregador
  assignBtn.addEventListener('click', () => {
    const detalhesEntregador = document.getElementById('detalhes-entregador');
    const orderId = detalhesEntregador.dataset.orderId;
    const csrfToken = detalhesEntregador.dataset.csrf;
    const selected = document.querySelector('input[name="selectedDeliveryMan"]:checked');

    if (!selected) { alert('Selecione um entregador antes de atribuir.'); return; }

    fetch(`/manager/assign_delivery/${orderId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ delivery_man_id: selected.value })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Entregador atribuído com sucesso!');
        location.reload();
      } else alert('Erro ao atribuir entregador.');
    })
    .catch(err => { console.error(err); alert('Erro ao atribuir entregador.'); });

    modal.style.display = 'none';
  });

});
