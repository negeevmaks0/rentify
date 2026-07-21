async function loadProfile(){

    const response = await fetch(
        "/api/users/profile/",
        {
            credentials:"include"
        }
    );


    if(!response.ok){

        window.location = "/login/";

        return;

    }


    const user = await response.json();


    document
    .getElementById("username")
    .value = user.username;


    document
    .getElementById("first_name")
    .value = user.first_name || "";


    document
    .getElementById("last_name")
    .value = user.last_name || "";


    document
    .getElementById("email")
    .value = user.email;


    document
    .getElementById("role")
    .value = user.role;

}



document
.getElementById("profileForm")
.addEventListener(
    "submit",
    async function(event){

        event.preventDefault();


        const response = await fetch(

            "/api/users/profile/",

            {
                method:"PATCH",

                credentials:"include",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    first_name:
                        document
                        .getElementById("first_name")
                        .value,

                    last_name:
                        document
                        .getElementById("last_name")
                        .value,

                    email:
                        document
                        .getElementById("email")
                        .value

                })

            }

        );


        const message =
            document
            .getElementById("message");


        if(response.ok){

            message
            .className =
            "mt-3 text-success";


            message.innerText =
            "Profile updated successfully.";

        }

        else{

            const data =
                await response.json();


            message
            .className =
            "mt-3 text-danger";


            message.innerText =
                JSON.stringify(data);

        }

    }
);


loadProfile();