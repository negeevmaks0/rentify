async function loadBookings(){


const container =
document.getElementById("bookings");


const response =
await fetch(
    "/api/bookings/",
    {
        credentials:"include"
    }
);



if(!response.ok){

    container.innerHTML =
    `
    <div class="alert alert-danger">
    Cannot load bookings
    </div>
    `;

    return;

}



const bookings =
await response.json();



if(bookings.length === 0){

    container.innerHTML =
    `
    <p>
    No bookings yet
    </p>
    `;

    return;

}



container.innerHTML = "";



bookings.forEach(booking => {


container.innerHTML += `


<div class="card mb-3">


<div class="card-body">


<h4>
${booking.property}
</h4>


<p>
${booking.start_date}
 →
${booking.end_date}
</p>


<p>
Price:
${booking.booking_price} €
</p>



<p>

Status:

<b>
${booking.status}
</b>


</p>



${
booking.status === "pending"

?

`

<button
class="btn btn-danger cancel-btn"
data-id="${booking.id}">

Cancel

</button>

`

:

""

}



</div>


</div>


`;


});



document
.querySelectorAll(".cancel-btn")
.forEach(btn=>{


btn.addEventListener(
"click",
()=>cancelBooking(btn.dataset.id)
);


});


}




async function cancelBooking(id){


const response =
await fetch(
`/api/bookings/${id}/cancel/`,
{

method:"PATCH",

credentials:"include"

}
);



if(response.ok){

    loadBookings();

}
else{

    const data =
    await response.json();

    alert(
        JSON.stringify(data)
    );

}


}



loadBookings();