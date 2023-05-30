document.addEventListener('DOMContentLoaded', function () {
    var cards = Array.from(document.getElementsByClassName('card-box'));
    var showMoreBtn = document.getElementById('show-more-btn');
    var showLessBtn = document.getElementById('show-less-btn');

    var maxCardsToShow = 2; // Change this value to control the number of cards to show initially
    var cardsToShow = maxCardsToShow;
    function showCards() {
        cards.forEach(function (card, index) {
            if (index < cardsToShow) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        if (cardsToShow >= cards.length) {
            showMoreBtn.style.display = 'none';
        } else {
            showMoreBtn.style.display = 'block';
        }

        if (cardsToShow <= maxCardsToShow) {
            showLessBtn.style.display = 'none';
        } else {
            showLessBtn.style.display = 'block';
        }
    }

    function showMore() {
        cardsToShow += maxCardsToShow;
        showCards();
    }

    function showLess() {
        cardsToShow = maxCardsToShow;
        showCards();
    }

    showCards();
    showMoreBtn.addEventListener('click', showMore);
    showLessBtn.addEventListener('click', showLess);
});


function showCards() {
    cards.forEach(function (card, index) {
        if (index < cardsToShow) {
            card.classList.remove('hidden'); // Remove the 'hidden' class
        } else {
            card.classList.add('hidden'); // Add the 'hidden' class
        }
    });
}