async function loadProperties(){

    const response = await fetch(
        "/api/properties/",
        {
            credentials:"include"
        }
    );


    const data = await response.json();


    const container =
        document.getElementById("properties");


    data.forEach(property => {


        container.innerHTML += `

        <div class="col-md-4">

            <div class="card p-3">

                <h5>
                    ${property.title}
                </h5>


                <p>
                    ${property.description}
                </p>


                <p>
                    ${property.location}
                </p>


                <strong>
                    ${property.price_per_month} €
                </strong>


            </div>

        </div>

        `;


    });


}


loadProperties();