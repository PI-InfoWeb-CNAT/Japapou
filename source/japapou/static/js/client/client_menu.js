document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".product-card");

  cards.forEach(card => {
    const media = parseFloat(card.dataset.media);
    const estrelas = card.querySelectorAll(".star");

    // sem média-> remove todas as estrelas
    if (!media || media <= 0) {
      estrelas.forEach(star => star.remove());
      return;
    }

    // remove as estrelas acima da média
    estrelas.forEach((star, index) => {
      if (index >= media) {
        star.remove();
      }
    });
  });
});
