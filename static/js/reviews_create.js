const bookingId =
    window.location.pathname.split("/")[3];


async function createReview(){

    const rating =
        document.getElementById("rating").value;


    const comment =
        document.getElementById("comment").value;


    const response =
        await fetch(
            "/api/reviews/",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                credentials:"include",

                body:JSON.stringify({
                    booking: bookingId,
                    rating: rating,
                    comment: comment
                })
            }
        );


    if(response.ok){

        window.location =
            "/bookings/";

    }

    else{

        const error =
            await response.json();

        alert(
            JSON.stringify(error)
        );

    }

}