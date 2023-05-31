var swiper = new Swiper(".mySwiper", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});


// Function to fetch the search results from the server
function fetchSearchResults(event) {
    event.preventDefault(); // Prevent form submission

    const form = document.getElementById("search-form");
    const formData = new FormData(form);

    // Convert form data to URL-encoded string
    const params = new URLSearchParams(formData).toString();

    // Make an AJAX request to the search-results URL with the form data
    fetch(`/search-results?${params}`)
        .then(response => response.json())
        .then(data => {
            // Update the HTML with the search results
            const serviceResults = document.getElementById("service-results");

            if (data.service_data.length > 0) {
                // Build the HTML for the search results
                let html = "";

                for (const service of data.service_data) {
                    html += `

            <div id="service-results" class="">
                <div class="card-box">
                    <div class="card">
                        <div>
                            <img src="https://images.pexels.com/photos/7755226/pexels-photo-7755226.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                                alt="">
                        </div>
                        <div class="card-info">
                        <h5>${service[0]} kr</h5>
                        <p>${service[1]} kr</p>
                        <p>${service[2]}</p>
                        <p>${service[3]}</p>
                        <p>${service[4]}</p>
                        <p>${service[5]}</p>
                        </div>
                        <div class="btn-section">
                            <a href="#" class="btn btn-dark">Boka</a>
                        </div>
                    </div>
            </div>
        </div>

            `;
                }

                // Update the serviceResults HTML
                serviceResults.innerHTML = html;
            } else {
                // Display a message if no matching services found
                serviceResults.innerHTML = "<p>No matching services found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching search results:", error);
        });
}

// Attach event listener to the form submission
const form = document.getElementById("search-form");
form.addEventListener("submit", fetchSearchResults);
