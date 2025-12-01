document.addEventListener('DOMContentLoaded', () => {

   // --- Coverflow ---
   const slides = document.querySelectorAll('.slide');
   const prevBtn = document.getElementById('prev');
   const nextBtn = document.getElementById('next');
   
   // Se houver menos de 3 slides, começa no 0, caso contrário, começa no 1
   let current = slides.length >= 3 ? 1 : 0; 
   
   // Apenas tentar calcular a largura se houver slides
   const slideWidth = slides.length > 0 ? slides[0].offsetWidth : 0;
   // Um pequeno ajuste no cálculo, pois 20 é o valor do margin/gap (assumido)
   const totalSlideWidth = slideWidth + 20; 
  
   function updateSlides() {
    slides.forEach((slide, i) => {
     const offset = i - current;
     const absOffset = Math.abs(offset);
     const maxVisible = 2; // Número máximo de slides visíveis em cada lado (além do central)
  
     if (absOffset > maxVisible) {
      slide.style.opacity = '0';
      slide.style.pointerEvents = 'none';
      // Reduzido para ser menos "visível"
      slide.style.transform = 'scale(0.5) translateX(0)'; 
      slide.style.zIndex = 0;
      return;
     }
  
     slide.style.opacity = '1';
     slide.style.pointerEvents = 'auto';
     // Z-index para simular profundidade (central é maior)
     slide.style.zIndex = 10 - absOffset; 
     
     // Aplica a transformação: 
     // Se for o slide central (offset === 0), não translada e escala em 1.
     // Caso contrário, translada pela distância e escala em 0.7.
     slide.style.transform = offset === 0 
      ? 'translateX(0) scale(1)' 
      : `translateX(${offset * totalSlideWidth}px) scale(0.7)`;
    });
   }
  
   // Adiciona listeners para os botões de navegação
   prevBtn.addEventListener('click', () => { 
    if(current > 0){
     current--; 
     updateSlides();
    }
   });
   
   nextBtn.addEventListener('click', () => { 
    if(current < slides.length - 1){
     current++; 
     updateSlides();
    }
   });
   
   // Inicializa o Coverflow
   if (slides.length > 0) {
     updateSlides();
   }
   
   // --- Confirmação de Entrega (LÓGICA CONSOLIDADA) ---
   const confirmBtn = document.getElementById('confirm-delivery-btn');
   const container = document.getElementById('confirm-delivery-container');
  
   if (!confirmBtn || !container) {
     return;
   }
  
   // 1. INICIALIZAÇÃO: Verifica o estado de entrega via data attributes do Django
   const deliveryStatus = container.dataset.deliveryStatus;
   const initialDeliveryDate = container.dataset.deliveryDate;
  
   if (deliveryStatus === 'ENTREGUE') {
     // Adiciona a classe e desabilita
     confirmBtn.disabled = true;
     confirmBtn.classList.add('ENTREGUE');
     
     // Atualiza o visual se a data inicial foi passada pelo Django
     if (initialDeliveryDate) {
       confirmBtn.innerHTML = `<h4>Entrega registrada (${initialDeliveryDate})</h4>`;
       confirmBtn.style.backgroundColor = '#3bb33b'; // Verde para sucesso
     }
   }
  
  
   // 2. Adicionar o listener para a requisição POST (AGORA SEM DUPLICAÇÃO)
   confirmBtn.addEventListener('click', async () => {
    // Evita múltiplas requisições se o botão estiver desabilitado ou já confirmado
    if (confirmBtn.disabled || confirmBtn.classList.contains('confirmed')) {
      return;
    }
    
    // Desabilitar enquanto a requisição está em andamento
    confirmBtn.disabled = true;
    confirmBtn.innerHTML = '<h4>Registrando...</h4>'; // Feedback de carregamento
  
    const orderId = container.dataset.orderId;
    const csrf = container.dataset.csrf;
  
    try {
     const response = await fetch(`/delivery_man/confirm_delivery/${orderId}/`, {
      method: 'POST',
      headers: {
       'X-CSRFToken': csrf,
       'Content-Type': 'application/json' 
      },
      body: JSON.stringify({}) 
     });
  
     const data = await response.json();
  
     if (data.status === 'ok') {
      // Formata a data recebida (data.delivery_date deve ser uma string ISO)
      const deliveryDate = new Date(data.delivery_date);
      const formattedDate = deliveryDate.toLocaleString('pt-BR', { 
        day: '2-digit', month: '2-digit', year: 'numeric', 
        hour: '2-digit', minute: '2-digit' 
      });
  
      confirmBtn.innerHTML = `<h4>Entrega registrada (${formattedDate})</h4>`;
      confirmBtn.style.backgroundColor = '#3bb33b'; // Verde para sucesso
      confirmBtn.classList.add('confirmed');
      // Mantém desabilitado após o sucesso
      confirmBtn.disabled = true; 
     } else {
      alert(data.message || 'Erro ao registrar entrega. Tente novamente.');
      confirmBtn.innerHTML = '<h4>Confirmar entrega</h4>'; // Volta ao texto original
      confirmBtn.disabled = false; // Habilita novamente
     }
    } catch (error) {
     console.error('Erro na requisição:', error);
     alert('Erro de conexão ou no servidor. Verifique o console.');
     confirmBtn.innerHTML = '<h4>Confirmar entrega</h4>'; // Volta ao texto original
     confirmBtn.disabled = false; // Habilita novamente
    }
   });
  
  });