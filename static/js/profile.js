async function loadProfile(){

    const response =
        await fetch(
            "/api/users/profile/",
            {
                credentials:"include"
            }
        );


    if(!response.ok){

        window.location =
            "/login/";

        return;

    }


    const user =
        await response.json();


    document
        .getElementById("username")
        .value =
        user.username;


    document
        .getElementById("first_name")
        .value =
        user.first_name || "";


    document
        .getElementById("last_name")
        .value =
        user.last_name || "";


    document
        .getElementById("email")
        .value =
        user.email;


    document
        .getElementById("role")
        .value =
        user.role;


    const fullName =
        `${user.first_name || ""} ${user.last_name || ""}`
        .trim();


    document
        .getElementById("profileName")
        .innerText =
        fullName ||
        user.username;


    document
        .getElementById("profileUsername")
        .innerText =
        `@${user.username}`;


    document
        .getElementById("avatarLetter")
        .innerText =
        (
            user.first_name ||
            user.username
        )
        .charAt(0)
        .toUpperCase();

}


document
    .getElementById("profileForm")
    .addEventListener(
        "submit",
        async function(event){

            event.preventDefault();


            const response =
                await fetch(

                    "/api/users/profile/",

                    {

                        method:"PATCH",

                        credentials:"include",

                        headers:{
                            "Content-Type":
                            "application/json"
                        },

                        body:JSON.stringify({

                            first_name:
                                document
                                .getElementById(
                                    "first_name"
                                )
                                .value,

                            last_name:
                                document
                                .getElementById(
                                    "last_name"
                                )
                                .value,

                            email:
                                document
                                .getElementById(
                                    "email"
                                )
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
                    "profile-message text-success";


                message
                    .innerText =
                    "Profile updated successfully.";


                loadProfile();

            }

            else{

                const data =
                    await response.json();


                message
                    .className =
                    "profile-message text-danger";


                message
                    .innerText =
                    data.detail ||
                    "Unable to update profile.";

            }

        }
    );


loadProfile();