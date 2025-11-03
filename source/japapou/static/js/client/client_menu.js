// document.addEventListener("DOMContentLoaded", () => {
//   const cards = document.querySelectorAll(".product-card");

//   cards.forEach(card => {
//     const media = parseFloat(card.dataset.media);
//     const estrelas = card.querySelectorAll(".star");

//     // sem média-> remove todas as estrelas
//     if (!media || media <= 0) {
//       estrelas.forEach(star => star.remove());
//       return;
//     }

//     // remove as estrelas acima da média
//     estrelas.forEach((star, index) => {
//       if (index >= media) {
//         star.remove();
//       }
//     });
//   });
// });





document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".product-card");

  cards.forEach(card => {
    // 1. Lemos a média (que será 0 se não houver avaliações)
    const media = parseFloat(card.dataset.media);
    
    // 2. Selecionamos todas as 5 estrelas DENTRO deste card
    const estrelas = card.querySelectorAll(".star");

    // 3. Iteramos por todas as 5 estrelas (index de 0 a 4)
    estrelas.forEach((star, index) => {
      
      // Se o 'index' da estrela for MAIOR ou IGUAL à média,
      // ela deve ser pintada de cinza (inativa).
      //
      // Exemplo (Média = 0):
      // Index 0: (0 >= 0) -> Adiciona .star-inactive (Cinza)
      // ... todas ficam cinza
      
      if (index >= media) {
        star.classList.add("star-inactive");
      }
      
      // As estrelas ativas (abaixo da média) simplesmente
      // não recebem a classe .star-inactive e ficam com a
      // cor amarela padrão que definimos no CSS.
    });
  });
});
