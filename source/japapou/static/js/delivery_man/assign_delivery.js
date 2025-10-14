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

      slide.style.transform = offset === 0 
        ? 'translateX(0) scale(1)' 
        : `translateX(${offset * slideWidth}px) scale(0.7)`;
    });
  }

  prevBtn.addEventListener('click', () => { if(current>0){current--; updateSlides();}});
  nextBtn.addEventListener('click', () => { if(current<slides.length-1){current++; updateSlides();}});
  updateSlides();

  // Confirmar entrega
  const confirmBtn = document.getElementById('confirm-delivery-btn');
  if (!confirmBtn) return;

  confirmBtn.addEventListener('click', async () => {
    const container = document.getElementById('confirm-delivery-container');
    const orderId = container.dataset.orderId;
    const csrf = container.dataset.csrf;

    try {
      const response = await fetch(`/delivery_man/assign_delivery/${orderId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (data.status === 'ok') {
        confirmBtn.innerHTML = `<h4>Entrega registrada (${data.delivery_date})</h4>`;
        confirmBtn.style.backgroundColor = '#3bb33b';
        confirmBtn.classList.add('confirmed');
        confirmBtn.disabled = true;
      } else {
        alert('Erro ao registrar entrega.');
      }
    } catch (error) {
      console.error(error);
      alert('Erro de conexão.');
    }
  });

});