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
                        class="btn btn-primary w-100 view-details"
                        data-id="${property.id}">
                        View details
                    </button>


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


                const id = button.dataset.id;


                const property =
                properties.find(
                    p => p.id == id
                );


                openPropertyModal(property);


            }
        );


    });


}

function openPropertyModal(property){


const modal =
document.getElementById("propertyModal");


const content =
document.getElementById("modalContent");



content.innerHTML = `

<h2>
${property.title}
</h2>


${
property.images.length

?

`
<div class="row g-2">

${property.images.map(
img =>

`
<div class="col-4">

<img 
src="${img.image}"
class="img-fluid rounded">

</div>

`

).join("")}

</div>
`

:

`
<img 
src="/static/images/no-image.jpg"
class="img-fluid rounded mb-3">
`

}



<p>
${property.description}
</p>


<p>
Location:
${property.location}
</p>


<p>
Rooms:
${property.room_count}
</p>


<h3>
${property.price_per_month} €
</h3>


<button 
class="btn btn-success"
onclick="goBooking(${property.id})">

Booking

</button>


`;



modal.style.display="flex";


}



function closePropertyModal(){

document.getElementById(
"propertyModal"
).style.display="none";

}



document
.getElementById("closeModal")
.onclick =
closePropertyModal;



function goBooking(id){

window.location =
`/bookings/create/${id}/`;

}


checkUser();
loadProperties();
