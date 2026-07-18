async function checkUser(){

    const response = await fetch(
        "/api/users/profile/",
        {
            credentials:"include"
        }
    );


    if(response.ok){

        const user = await response.json();


        if(user.role === "landlord"){

            document
            .getElementById("createButton")
            .classList
            .remove("d-none");

        }

    }

}

async function loadProperties(){

    const container = document.getElementById("properties");

    container.innerHTML = "";


    const response = await fetch(
        "/api/properties/",
        {
            credentials:"include"
        }
    );


    const properties = await response.json();



    properties.forEach(property => {


        const image = property.main_image
            ?
            property.main_image
            :
            "/static/images/no-image.jpg";



        container.innerHTML += `


        <div class="col-md-4">


            <div class="card property-card h-100">


                <img 
                    src="${image}"
                    class="card-img-top property-image"
                    alt="${property.title}"
                >



                <div class="card-body">


                    <h5 class="card-title">
                        ${property.title}
                    </h5>



                    <p class="text-muted">
                        ${property.location}
                    </p>



                    <p>
                        ${property.description}
                    </p>



                    <p>
                        Rooms:
                        ${property.room_count}
                    </p>



                    <p>
                        Type:
                        ${property.property_type}
                    </p>



                    <h5>
                        ${property.price_per_month} €
                        <small>
                            / month
                        </small>
                    </h5>



                    <button 
                        class="btn btn-primary w-100">
                        View details
                    </button>


                </div>


            </div>


        </div>


        `;


    });


}


checkUser();
loadProperties();
