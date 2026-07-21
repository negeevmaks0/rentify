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



const uploadStatus =
    document.getElementById(
        "uploadStatus"
    );

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

    uploadStatus.innerHTML = `

    <div class="alert alert-info">

        ⏳ Uploading ${files.length} image(s)...

    </div>

    `;



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

    uploadStatus.innerHTML = `

    <div class="alert alert-success">

        ✅ ${files.length} image(s) uploaded successfully!

    </div>

    `;


}



window.location="/properties/";



});

document
.getElementById("images")
.addEventListener(
"change",
function(){

    const preview =
        document.getElementById(
            "imagePreview"
        );


    preview.innerHTML = "";


    Array.from(this.files)
    .forEach(file => {


        const item =
        document.createElement(
            "div"
        );


        item.className =
        "mb-2 text-secondary";


        item.innerHTML =
        `
        📷 ${file.name}
        (${Math.round(file.size / 1024)} KB)
        `;


        preview.appendChild(item);

    });


});