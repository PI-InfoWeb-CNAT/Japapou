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

    if (!selected) { 
      // alert('Selecione um entregador antes de atribuir.');
      return; }

    fetch(`/manager/assign_delivery/${orderId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify({ delivery_man_id: selected.value })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // alert('Entregador atribuído com sucesso!');
        location.reload();
      } 
      // else 
      //   alert('Erro ao atribuir entregador.');
    })
    .catch(err => { 
      console.error(err); 
      // alert('Erro ao atribuir entregador.'); 
    });

    modal.style.display = 'none';
  });

});

document.addEventListener('DOMContentLoaded', () => {
  const confirmBtn = document.getElementById('button-3');
  
  // Se o botão não existir ou já tiver a classe 'confirmed', paramos aqui.
  if (!confirmBtn || confirmBtn.classList.contains('confirmed')) return;

  confirmBtn.addEventListener('click', async () => {
    const container = document.getElementById('detalhes-entregador');
    const orderId = container.dataset.orderId;
    const csrf = container.dataset.csrf;

    // Feedback visual imediato: "Carregando..."
    const originalText = confirmBtn.innerHTML;
    confirmBtn.innerHTML = '<h4>Processando...</h4>';
    confirmBtn.style.pointerEvents = 'none'; // Evita cliques duplos

    try {
      const response = await fetch(`/manager/confirm_dispatch/${orderId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (data.status === 'ok') {
        const agora = new Date();
        const dataFormatada = agora.toLocaleDateString('pt-BR') + ' às ' + agora.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});
        
        // --- MUDANÇA VISUAL AQUI ---
        // 1. Usamos <br> para quebrar a linha.
        // 2. Usamos um <span> com fonte menor para a data.
        confirmBtn.innerHTML = `
            <h4 style="margin: 0;">Já saiu para entrega</h4>
            <span style="font-size: 1.2em; font-weight: normal; display: block;>
                ${dataFormatada}
            </span>
        `;
        
        confirmBtn.classList.add('confirmed');
        
        // --- AJUSTES DE CSS NO JS ---
        confirmBtn.style.backgroundColor = '#3bb33b';
        confirmBtn.style.opacity = '1';
        
        // Importante: removemos a altura fixa e damos espaço interno
        confirmBtn.style.height = 'auto'; 
        confirmBtn.style.padding = '30px 10px'; 
        confirmBtn.style.display = 'flex';
        confirmBtn.style.flexDirection = 'column';
        confirmBtn.style.justifyContent = 'center';
        confirmBtn.style.alignItems = 'center';

        // Esconder o botão de alterar (mantém-se igual)
        const changeBtn = container.querySelector('.assign-delivery-btn');
        if (changeBtn) {
            changeBtn.closest('.button').style.display = 'none';
        }

      } else {
        // Se der erro no servidor
        confirmBtn.innerHTML = originalText;
        confirmBtn.style.pointerEvents = 'auto';
        alert('Erro ao confirmar saída.');
      }
    } catch (error) {
      console.error(error);
      confirmBtn.innerHTML = originalText;
      confirmBtn.style.pointerEvents = 'auto';
      alert('Erro de conexão.');
    }
  });
});
