document.addEventListener("DOMContentLoaded", () => {
    const addCard = document.getElementById("add-card");

    if (addCard) {
        addCard.addEventListener("mousedown", () => {
            addCard.style.transform = "scale(0.97)";
        });
        addCard.addEventListener("mouseup", () => {
            addCard.style.transform = "scale(1)";
        });
    }
});
