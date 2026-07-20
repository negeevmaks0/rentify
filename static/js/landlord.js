async function loadLandlord(){


const response = await fetch(
"/api/properties/my/",
{
credentials:"include"
}
);


const properties = await response.json();


document.getElementById("properties").innerHTML =
properties.map(p=>`

<div class="card mb-3">

<div class="card-body">

<h5>
${p.title}
</h5>

<p>
${p.location}
</p>

</div>

</div>

`).join("");



const bookingsResponse = await fetch(
"/api/bookings/landlord/",
{
credentials:"include"
}
);


const bookings = await bookingsResponse.json();


document.getElementById("requests").innerHTML =
bookings.map(b=>`

<div class="card mb-3">

<div class="card-body">

<h5>
${b.property_detail.title}
</h5>

<p>
${b.start_date}
-
${b.end_date}
</p>


<p>
Status:
${b.status}
</p>


${
b.status==="pending"

?

`

<button
class="btn btn-success"
onclick="approve(${b.id})">

Approve

</button>


<button
class="btn btn-danger"
onclick="reject(${b.id})">

Reject

</button>

`

:""

}


</div>

</div>

`).join("");

}



async function approve(id){

await fetch(
`/api/bookings/${id}/approve/`,
{
method:"PATCH",
credentials:"include"
}
);

loadLandlord();

}



async function reject(id){

await fetch(
`/api/bookings/${id}/reject/`,
{
method:"PATCH",
credentials:"include"
}
);

loadLandlord();

}



loadLandlord();