console.log("Booking page");

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener("DOMContentLoaded", async () => {
    const propertyElement =
        document.getElementById("propertyId");

    if (!propertyElement) {
        console.error("Property ID not found");
        return;
    }

    const propertyId =
        propertyElement.dataset.id;
    const container = document.getElementById("propertyContainer");

    try {
        const response = await fetch(`/api/properties/${propertyId}/`);

        if (!response.ok) {
            throw new Error("Property not found");
        }

        const property = await response.json();

        container.innerHTML = `
            <div class="booking-create-header">
                <h1>
                    Book this property
                </h1>

                <p>
                    Choose your dates and confirm your reservation.
                </p>
            </div>

            <div class="booking-gallery">
                ${property.images.map(img => `
                    <img
                        src="${img.image}"
                        class="booking-gallery-image">
                `).join("")}
            </div>

            <div class="booking-property-info">
                <h2>
                    ${property.title}
                </h2>

                <p class="booking-location">
                    📍 ${property.location}
                </p>

                <p>
                    ${property.description}
                </p>

                <div class="booking-details">
                    <div>
                        <span>
                            Rooms
                        </span>

                        <strong>
                            ${property.room_count}
                        </strong>
                    </div>

                    <div>
                        <span>
                            Price
                        </span>

                        <strong>
                            ${property.price_per_night} € / night
                        </strong>
                    </div>
                </div>
            </div>

            <div class="booking-divider"></div>

            <div class="booking-date-grid">
                <div class="booking-field">
                    <label>
                        Check in
                    </label>

                    <input
                        type="date"
                        id="startDate">
                </div>

                <div class="booking-field">
                    <label>
                        Check out
                    </label>

                    <input
                        type="date"
                        id="endDate">
                </div>
            </div>

            <div class="booking-summary">
                <div>
                    <span>
                        Nights
                    </span>

                    <strong id="nightCount">
                        0
                    </strong>
                </div>

                <div>
                    <span>
                        Total
                    </span>

                    <strong>
                        <span id="totalPrice">
                            0
                        </span>
                        €
                    </strong>
                </div>
            </div>

            <button
                class="btn btn-primary booking-button"
                id="bookingBtn"
                disabled>
                Book property
            </button>

            <div
                id="bookingError"
                class="booking-error">
            </div>
        `;

        const startInput =
        document.getElementById("startDate");

        const endInput =
        document.getElementById("endDate");

        const nightsText =
        document.getElementById("nightCount");

        const totalText =
        document.getElementById("totalPrice");

        const bookingBtn =
        document.getElementById("bookingBtn");

        function calculatePrice(){
            if(
                !startInput.value ||
                !endInput.value
            ){
                return;
            }

            const today =
            new Date();

            today.setHours(0,0,0,0);

            if(startInput.value){
                const selected =
                    new Date(startInput.value);

                if(selected < today){
                    startInput.value = "";
                    bookingBtn.disabled = true;

                    return;
                }
            }

            const start = new Date(startInput.value);

            const end = new Date(endInput.value);

            const diff = (end-start)/(1000*60*60*24);

            if(diff <= 0){
                nightsText.innerText = 0;
                totalText.innerText = 0;
                bookingBtn.disabled = true;

                return;
            }

            nightsText.innerText = diff;
            totalText.innerText = diff * Number(property.price_per_night);
            bookingBtn.disabled = false;
        }

        startInput.addEventListener(
            "change",
            calculatePrice
        );

        endInput.addEventListener(
            "change",
            calculatePrice
        );

        bookingBtn.addEventListener(
        "click",
        async ()=>{
            bookingBtn.disabled = true;
            bookingBtn.innerText = "Creating booking...";

            const response =
            await fetch(
                "/api/bookings/",
                {

                method:"POST",

                credentials:"include",

                headers:{
                    "Content-Type":"application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body:JSON.stringify({
                    property:property.id,
                    start_date:startInput.value,
                    end_date:endInput.value
                })
            });

            if(response.ok){
                alert("Booking created");

                window.location="/bookings/";

                return;
            }

            const data = await response.json();

            const errorBox =
            document.getElementById("bookingError");

            if(data.non_field_errors){
                errorBox.innerText =
                data.non_field_errors[0];
            }

            else if(data.detail){
                errorBox.innerText =
                data.detail;
            }

            else{
                errorBox.innerText =
                "Booking error";
            }

            bookingBtn.disabled = false;
            bookingBtn.innerText = "Book property";
        });

    } catch(error) {
        console.error(error);

        container.innerHTML = `
            <div class="alert alert-danger">
                Cannot load property
            </div>
        `;
    }
});