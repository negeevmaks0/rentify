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

price_per_month:
document.getElementById("price").value,

room_count:
document.getElementById("rooms").value,

property_type:
document.getElementById("type").value

})

});


if(response.ok){


const property = await response.json();


const files =
document.getElementById("images").files;


for(
let file of files
){

const formData = new FormData();


formData.append(
"property",
property.id
);


formData.append(
"image",
file
);



await fetch(
"/api/properties/images/",
{

method:"POST",

credentials:"include",

body:formData

}

);


}


window.location="/properties/";

}


else{

const data =
await response.json();


document.getElementById("error").innerText =
JSON.stringify(data);

}


});