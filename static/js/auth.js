document
.getElementById("loginForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const response = await fetch(
        "/api/users/login/",
        {
            method:"POST",

            credentials:"include",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                username:
                    document.getElementById("username").value,

                password:
                    document.getElementById("password").value

            })
        }
    );

    if(response.ok){

        window.location="/";

    }

    else{

        document.getElementById("error").innerText =
            "Wrong username or password.";

    }

});