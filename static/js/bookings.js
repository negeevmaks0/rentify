console.log("Booking page");


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


                    <button 
                        class="btn btn-primary"
                        id="bookingBtn"
                    >
                        Book property
                    </button>

                </div>

            </div>

        `;


        document
            .getElementById("bookingBtn")
            .addEventListener("click", () => {

                console.log("Booking clicked");

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