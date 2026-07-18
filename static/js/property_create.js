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

title: document.getElementById("title").value,

description: document.getElementById("description").value,

location: document.getElementById("location").value,

price_per_month: document.getElementById("price").value,

room_count: document.getElementById("rooms").value,

property_type: document.getElementById("type").value

})


});


if(response.ok){

window.location="/properties/";

}

else{

const data = await response.json();

error.innerText =
JSON.stringify(data);

}


});