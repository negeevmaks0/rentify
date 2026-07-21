let allProperties = [];


async function loadProperties(){

    const container =
        document.getElementById("properties");


    try{

        const response = await fetch(
            "/api/properties/",
            {
                credentials:"include"
            }
        );


        if(!response.ok){

            throw new Error(
                "Failed to load properties."
            );

        }


        allProperties =
            await response.json();


        renderProperties(
            allProperties
        );


    }catch(error){

        console.error(error);

        container.innerHTML = `

            <div class="col-12">

                <div class="empty-state">

                    <h4>
                        Unable to load properties
                    </h4>

                    <p>
                        Please try again later.
                    </p>

                </div>

            </div>

        `;

    }

}


function renderProperties(properties){

    const container =
        document.getElementById("properties");


    const emptyState =
        document.getElementById("emptyState");


    const count =
        document.getElementById("propertyCount");


    container.innerHTML = "";

    if(!properties.length){

        emptyState
            .classList
            .remove("d-none");

        return;

    }


    emptyState
        .classList
        .add("d-none");


    properties.forEach(property => {


        const image =
            property.main_image
            ||
            "/static/images/no-image.jpg";


        container.innerHTML += `

            <div class="col-md-6 col-xl-4">


                <div class="property-card
                            property-list-card
                            h-100">


                    <div class="property-image-wrapper">

                        <img
                            src="${image}"
                            class="property-image"
                            alt="${property.title}">


                        <span
                            class="property-type-badge
                                   property-card-badge">

                            ${property.property_type}

                        </span>

                    </div>


                    <div class="card-body">


                        <h5 class="card-title">

                            ${property.title}

                        </h5>


                        <p class="property-location">

                            📍 ${property.location}

                        </p>


                        <p class="property-description">

                            ${property.description}

                        </p>


                        <div class="property-card-footer">


                            <div>

                                <span
                                    class="property-price">

                                    ${property.price_per_night} €

                                </span>

                                <small
                                    class="text-secondary">

                                    / night

                                </small>

                            </div>


                            <button
                                class="btn btn-primary
                                       view-details"
                                data-id="${property.id}">

                                View details

                            </button>


                        </div>


                    </div>


                </div>


            </div>

        `;

    });


    document
        .querySelectorAll(".view-details")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const id =
                        button.dataset.id;


                    const property =
                        allProperties.find(
                            property =>
                            property.id == id
                        );


                    openPropertyModal(
                        property
                    );

                }
            );

        });

}


function openPropertyModal(property){

    const modal =
        document.getElementById(
            "propertyModal"
        );


    const content =
        document.getElementById(
            "modalContent"
        );


    const images =
        property.images.length

        ?

        `

            <div
                class="property-modal-gallery">

                ${property.images.map(
                    image => `

                    <img
                        src="${image.image}"
                        class="property-modal-image">

                `
                ).join("")}

            </div>

        `

        :

        `

            <img
                src="/static/images/no-image.jpg"
                class="property-modal-main-image">

        `;


    content.innerHTML = `

        ${images}


        <div
            class="property-modal-details">


            <span
                class="property-type-badge">

                ${property.property_type}

            </span>


            <h2>

                ${property.title}

            </h2>


            <p
                class="property-location">

                📍 ${property.location}

            </p>


            <p
                class="property-modal-description">

                ${property.description}

            </p>


            <div
                class="property-details-grid">


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
                        ${property.price_per_night} €
                        <small>/ night</small>
                    </strong>

                </div>


            </div>


            <button
                class="btn btn-success
                       btn-lg
                       w-100"
                onclick="goBooking(${property.id})">

                Request booking

            </button>


        </div>

    `;


    modal.style.display =
        "flex";

}


function closePropertyModal(){

    document
        .getElementById(
            "propertyModal"
        )
        .style.display =
        "none";

}


document
    .getElementById(
        "closeModal"
    )
    .onclick =
    closePropertyModal;


document
    .getElementById(
        "propertySearch"
    )
    .addEventListener(
        "input",
        function(){

            const search =
                this.value
                    .toLowerCase()
                    .trim();


            const filtered =
                allProperties.filter(
                    property =>

                        property.title
                            .toLowerCase()
                            .includes(search)

                        ||

                        property.location
                            .toLowerCase()
                            .includes(search)

                        ||

                        property.description
                            .toLowerCase()
                            .includes(search)
                );


            renderProperties(
                filtered
            );

        }
    );


function goBooking(id){

    window.location =
        `/bookings/create/${id}/`;

}


window.addEventListener(
    "click",
    function(event){

        const modal =
            document.getElementById(
                "propertyModal"
            );


        if(event.target === modal){

            closePropertyModal();

        }

    }
);


loadProperties();