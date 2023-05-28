
const open = document.getElementById('open');
const modal_container = document.getElementById('modal_container');
const close = document.getElementById('close');

open.addEventListener('click', () => {
    modal_container.classList.add('show');
});

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
});

function handleButtonClick(event) {
    const button = event.target
    const tags = button.getAttribute('data-tags');


    fetch('/tag_buttons/${tags}')
        .then(response => response.json())
        .then(data =>{
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
    button.addEventListener('click', handleButtonClick);
});
