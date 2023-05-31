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

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
});

function handleButtonClick(event) {
    const button = event.target
    const tags = button.getAttribute('data-tags');

    const form = document.getElementById('tag_search_form');
    form.action = form.action.slice(0, -1) + tags;

    fetch('/tag_buttons/${tags}')
        .then(response => response.json())
        .then(data => {
            const searchResultsDiv = document.getElementById('search-results');
            searchResultsDiv.innerHTML = '';


            if (data.length > 0) {
                const resultsList = document.createElement('ul');


                data.forEach(result => {
                    const listItem = document.createElement('li');
                    listItem.textContent = result;
                    resultsList.appendChild(listItem);

                });
                searchResultsDiv.appendChild(resultsList);

            } else {
                searchResultsDiv.textContent = 'No matching services found';
            }
        })
        .catch(error => {
            console.error(error);
        });
}

const buttons = document.querySelectorAll('.tag_btn');
buttons.forEach(button => {
    button.addEventListener('click', event => handleButtonClick(event));
});

