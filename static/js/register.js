document
.getElementById("registerForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const response = await fetch(
        "/api/users/register/",
        {
            method:"POST",

            credentials:"include",

            headers:{
                "Content-Type":"application/json"
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

        }
    );

    if(response.ok){

        window.location="/";

    }

    else{

        const data=await response.json();

        error.innerText=
            JSON.stringify(data);

    }

});