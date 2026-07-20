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

    const propertyText = document.getElementById("propertyId").textContent;

    const propertyId = propertyText.replace(/\D/g, "");

    const container = document.getElementById("propertyContainer");


    try {

        const response = await fetch(`/api/properties/${propertyId}/`);

        if (!response.ok) {
            throw new Error("Property not found");
        }


        const property = await response.json();


        container.innerHTML = `

            <div class="card">

                <div id="propertyImages">

                    ${property.images.map(img => `

                        <img 
                            src="${img.image}"
                            class="img-thumbnail m-2"
                            style="
                                width:250px;
                                height:180px;
                                object-fit:cover;
                            "
                        >

                    `).join("")}

                </div>


                <div class="card-body">

                    <h3>
                        ${property.title}
                    </h3>


                    <p>
                        ${property.description}
                    </p>


                    <p>
                        📍 ${property.location}
                    </p>


                    <p>
                        🏠 Rooms: ${property.room_count}
                    </p>


                    <h4>
                        ${property.price_per_night} € / night
                    </h4>

                    <hr>

                    <div class="mb-3">

                        <label>
                            Check in
                        </label>

                        <input
                            type="date"
                            id="startDate"
                            class="form-control">

                    </div>

                    <div class="mb-3">

                        <label>
                            Check out
                        </label>

                        <input
                            type="date"
                            id="endDate"
                            class="form-control">

                    </div>

                    <p>

                        Nights:
                        <span id="nightCount">
                            0
                        </span>

                    </p>

                    <h4>

                        Total:
                        <span id="totalPrice">
                            0
                        </span>
                        €

                    </h4>

                    <button
                        class="btn btn-success"
                        id="bookingBtn"
                        disabled>

                        Book property

                    </button>

                    <div
                        id="bookingError"
                        class="text-danger mt-2">
                    </div>

                </div>

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

            const start =
                new Date(startInput.value);

            const end =
                new Date(endInput.value);

            const diff =
                (end-start)/(1000*60*60*24);

            if(diff <= 0){

                nightsText.innerText = 0;

                totalText.innerText = 0;

                bookingBtn.disabled = true;

                return;

            }

            nightsText.innerText = diff;

            totalText.innerText =
                diff * Number(property.price_per_night);

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

            const data =
                await response.json();

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