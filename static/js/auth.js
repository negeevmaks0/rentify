async function checkAuth() {

    const navbar = document.getElementById("navbar");

    if (!navbar) {
        return;
    }


    try {

        const response = await fetch(
            "/api/users/profile/",
            {
                credentials: "include"
            }
        );


        if (response.ok) {

            const user = await response.json();


            navbar.innerHTML = `

                <a href="/" class="nav-link">
                    Home
                </a>

                <a href="/properties/" class="nav-link">
                    Properties
                </a>

                <a href="/bookings/" class="nav-link">
                    My bookings
                </a>

                <a href="/profile/" class="nav-link">
                    ${user.username}
                </a>

                <button
                    id="logoutBtn"
                    class="btn btn-outline-light ms-2">
                    Logout
                </button>

            `;


            document
                .getElementById("logoutBtn")
                .addEventListener(
                    "click",
                    logout
                );


        } else {


            navbar.innerHTML = `

                <a href="/login/" class="nav-link">
                    Login
                </a>

                <a href="/register/" class="nav-link">
                    Register
                </a>

            `;


        }


    } catch(error) {

        console.log(error);

    }

}



async function logout(){


    await fetch(
        "/api/users/logout/",
        {
            method:"POST",
            credentials:"include",
        }
    );


    window.location="/login/";

}



document.addEventListener(
    "DOMContentLoaded",
    checkAuth
);