document.addEventListener(
    "DOMContentLoaded",
    () => {


    const form =
        document.getElementById(
            "registerForm"
        );


    if(!form){
        return;
    }



    const message =
        document.getElementById(
            "message"
        );



    form.addEventListener(
        "submit",
        async function(event){


        event.preventDefault();



        message.innerText =
            "Creating account...";

        message.style.color =
            "#94a3b8";



        try{


            const response =
                await fetch(
                    "/api/users/register/",
                    {

                    method:"POST",

                    credentials:"include",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },


                    body:JSON.stringify({

                        username:
                            username.value,

                        first_name:
                            first_name.value,

                        last_name:
                            last_name.value,

                        email:
                            email.value,

                        password:
                            password.value,

                        role:
                            role.value

                    })


                });



            const data =
                await response.json();



            if(response.ok){


                message.style.color =
                    "#4ade80";


                message.innerText =
                    "Account created successfully.";


                setTimeout(
                    ()=>{
                        window.location="/";
                    },
                    800
                );


                return;

            }



            message.style.color =
                "#f87171";


            message.innerText =
                formatErrors(data);



        }

        catch(error){


            console.error(error);


            message.style.color =
                "#f87171";


            message.innerText =
                "Something went wrong. Please try again.";

        }


    });


});



function formatErrors(errors){


    if(errors.detail){
        return errors.detail;
    }


    let result = [];


    Object.keys(errors)
    .forEach(
        field=>{


        if(Array.isArray(errors[field])){


            errors[field].forEach(
                error=>{


                result.push(
                    `${field}: ${error}`
                );


            });

        }


    });



    return result.join("\n")
        ||
        "Registration failed.";

}