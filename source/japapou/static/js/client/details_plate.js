document.addEventListener('DOMContentLoaded', function() {
        const starWidget = document.getElementById('star-widget');
        if (starWidget) {
            const stars = starWidget.querySelectorAll('.star');
            const hiddenInput = document.getElementById('id_nota'); 

            function setStarRating(rating) {
                stars.forEach(star => {
                    const starValue = parseInt(star.dataset.value);
                    if (starValue <= rating) {
                        star.classList.add('filled');
                    } else {
                        star.classList.remove('filled');
                    }
                });
            }

            starWidget.addEventListener('click', function(e) {
                if (e.target.classList.contains('star')) {
                    const rating = parseInt(e.target.dataset.value);
                    hiddenInput.value = rating; 
                    setStarRating(rating);
                }
            });

            starWidget.addEventListener('mouseover', function(e) {
                if (e.target.classList.contains('star')) {
                    const hoverRating = parseInt(e.target.dataset.value);
                    setStarRating(hoverRating);
                }
            });

            starWidget.addEventListener('mouseout', function() {
                const currentRating = parseInt(hiddenInput.value) || 0;
                setStarRating(currentRating);
            });

            const initialRating = parseInt(hiddenInput.value) || 0;
            setStarRating(initialRating);
        }
    });