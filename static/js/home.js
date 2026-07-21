async function loadFeaturedProperties() {

    const container =
        document.getElementById(
            "featuredProperties"
        );


    try {

        const response = await fetch(
            "/api/properties/",
            {
                credentials: "include"
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load properties"
            );

        }


        const properties =
            await response.json();


        const featured =
            properties.slice(0, 3);


        container.innerHTML = "";


        if (featured.length === 0) {

            container.innerHTML = `

                <div class="col-12">

                    <div class="empty-state">

                        <h4>
                            No properties yet
                        </h4>

                        <p>
                            New properties will appear here soon.
                        </p>

                    </div>

                </div>

            `;

            return;

        }


        featured.forEach(property => {

            const image =
                property.main_image
                ||
                "/static/images/no-image.jpg";


            container.innerHTML += `

                <div class="col-md-6 col-lg-4">

                    <div class="property-card home-property-card">

                        <img
                            src="${image}"
                            class="property-image"
                            alt="${property.title}"
                        >


                        <div class="p-4">

                            <div class="d-flex
                                        justify-content-between
                                        align-items-start
                                        mb-2">

                                <h4>
                                    ${property.title}
                                </h4>

                                <span class="property-type-badge">

                                    ${property.property_type}

                                </span>

                            </div>


                            <p class="property-location">

                                📍 ${property.location}

                            </p>


                            <p class="property-description">

                                ${property.description}

                            </p>


                            <div class="d-flex
                                        justify-content-between
                                        align-items-center
                                        mt-4">

                                <div>

                                    <strong class="property-price">

                                        ${property.price_per_night} €

                                    </strong>

                                    <span class="text-secondary">

                                        / night

                                    </span>

                                </div>


                                <a
                                    href="/properties/"
                                    class="btn btn-primary">

                                    View

                                </a>

                            </div>

                        </div>

                    </div>

                </div>

            `;

        });


    } catch (error) {

        console.error(
            "Error loading featured properties:",
            error
        );


        container.innerHTML = `

            <div class="col-12">

                <div class="empty-state">

                    <p>
                        Unable to load properties.
                    </p>

                </div>

            </div>

        `;

    }

}

async function checkGetStartedButton() {

    const button =
        document.getElementById(
            "getStartedButton"
        );


    if (!button) {

        return;

    }


    const response = await fetch(
        "/api/users/profile/",
        {
            credentials: "include"
        }
    );


    if (response.ok) {

        button.remove();

    }

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadFeaturedProperties();
        checkGetStartedButton();

    }
);