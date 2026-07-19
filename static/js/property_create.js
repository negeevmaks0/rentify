document
.getElementById("propertyForm")
.addEventListener(
"submit",
async function(e){

e.preventDefault();



const response = await fetch(
    "/api/properties/",
    {

    method:"POST",

    credentials:"include",

    headers:{
        "Content-Type":"application/json"
    },


    body:JSON.stringify({

        title:
            document.getElementById("title").value,

        description:
            document.getElementById("description").value,

        location:
            document.getElementById("location").value,

        price_per_night:
            document.getElementById("price").value,

        room_count:
            document.getElementById("rooms").value,

        property_type:
            document.getElementById("type").value

    })

});



if(!response.ok){

    const data = await response.json();

    error.innerText =
        JSON.stringify(data);

    return;

}



const property = await response.json();



const files =
    document
    .getElementById("images")
    .files;



if(files.length > 0){


    const formData = new FormData();



    for(
        let i = 0;
        i < files.length;
        i++
    ){

        formData.append(
            "images",
            files[i]
        );

    }



    const uploadResponse = await fetch(

        `/api/properties/${property.id}/upload_image/`,

        {

        method:"POST",

        credentials:"include",

        body:formData

        }

    );



    if(!uploadResponse.ok){

        const data =
            await uploadResponse.json();


        error.innerText =
            JSON.stringify(data);

        return;

    }


}



window.location="/properties/";



});