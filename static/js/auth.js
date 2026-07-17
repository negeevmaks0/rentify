document
.getElementById("loginForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const response = await fetch(
        "/api/users/login/",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                username:
                    document.getElementById("email").value,

                password:
                    document.getElementById("password").value

            })
        }
    );

    const data = await response.json();


    if(response.ok){

        document.cookie = 
            `access=${data.access}; path=/; max-age=3600`;

        document.cookie =
            `refresh=${data.refresh}; path=/; max-age=604800`;


        window.location="/";

    }

    else{

        document.getElementById("error").innerText =
            data.detail || "Wrong email or password.";

    }

});