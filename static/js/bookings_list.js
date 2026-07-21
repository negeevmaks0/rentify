let currentFilter = "";



async function loadBookings(filter = ""){

    const container =
        document.getElementById("bookings");

    const emptyState =
        document.getElementById("emptyState");

    const count =
        document.getElementById("bookingCount");


    currentFilter = filter;


    container.innerHTML = `

        <div class="col-12 text-center">

            <p class="text-secondary">
                Loading bookings...
            </p>

        </div>

    `;


    try{

        const response =
            await fetch(
                `/api/bookings/?filter=${filter}`,
                {
                    credentials:"include"
                }
            );


        if(!response.ok){

            throw new Error(
                "Failed to load bookings"
            );

        }


        const bookings =
            await response.json();


        count.innerText =
            `${bookings.length} bookings`;


        if(!bookings.length){

            container.innerHTML = "";

            emptyState
                .classList
                .remove("d-none");

            return;

        }


        emptyState
            .classList
            .add("d-none");


        renderBookings(bookings);


    }catch(error){

        console.error(error);


        container.innerHTML = `

            <div class="col-12">

                <div class="empty-state">

                    <h4>
                        Unable to load bookings
                    </h4>

                    <p>
                        Please try again later.
                    </p>

                </div>

            </div>

        `;

    }

}



function renderBookings(bookings){

    const container =
        document.getElementById("bookings");


    container.innerHTML = "";


    bookings.forEach(booking => {

        const property =
            booking.property_detail;


        const image =
            property.main_image
            ||
            "/static/images/no-image.jpg";


        const statusClass =
            `booking-status-${booking.status}`;


        const canCancel =
            booking.status === "pending";


        container.innerHTML += `

            <div class="col-md-6 col-xl-4">

                <div class="booking-card h-100">


                    <div class="booking-image-wrapper">

                        <img
                            src="${image}"
                            class="booking-image"
                            alt="${property.title}">


                        <span
                            class="booking-status
                                   ${statusClass}">

                            ${booking.status}

                        </span>

                    </div>


                    <div class="booking-card-body">


                        <h4>
                            ${property.title}
                        </h4>


                        <p class="property-location">

                            📍 ${property.location}

                        </p>


                        <div class="booking-dates">

                            <div>

                                <span>
                                    Check-in
                                </span>

                                <strong>
                                    ${booking.start_date}
                                </strong>

                            </div>


                            <div class="booking-arrow">

                                →

                            </div>


                            <div>

                                <span>
                                    Check-out
                                </span>

                                <strong>
                                    ${booking.end_date}
                                </strong>

                            </div>

                        </div>


                        <div class="booking-info-grid">


                            <div>

                                <span>
                                    Nights
                                </span>

                                <strong>
                                    ${booking.nights}
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Total
                                </span>

                                <strong>
                                    ${booking.booking_price} €
                                </strong>

                            </div>


                        </div>


                        ${
                            canCancel

                            ?

                            `

                            <button
                                class="btn btn-outline-danger
                                       w-100
                                       cancel-btn"
                                data-id="${booking.id}">

                                Cancel booking

                            </button>

                            `

                            :

                            ""

                        }


                    </div>

                </div>

            </div>

        `;

    });


    document
        .querySelectorAll(".cancel-btn")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => cancelBooking(
                    button.dataset.id
                )
            );

        });

}



async function cancelBooking(id){

    const confirmed =
        confirm(
            "Are you sure you want to cancel this booking?"
        );


    if(!confirmed){

        return;

    }


    const response =
        await fetch(

            `/api/bookings/${id}/cancel/`,

            {

                method:"PATCH",

                credentials:"include"

            }

        );


    if(response.ok){

        loadBookings(currentFilter);

    }

    else{

        const data =
            await response.json();


        alert(
            data.detail
            ||
            "Unable to cancel booking."
        );

    }

}



document
    .querySelectorAll(".booking-filter")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(
                        ".booking-filter"
                    )
                    .forEach(
                        btn =>
                        btn.classList.remove(
                            "active"
                        )
                    );


                button
                    .classList
                    .add("active");


                loadBookings(
                    button.dataset.filter
                );

            }
        );

    });



loadBookings();